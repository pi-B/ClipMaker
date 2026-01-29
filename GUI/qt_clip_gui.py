from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QComboBox, QListWidget, QInputDialog, QSlider, QListWidgetItem, QMenuBar, QDialog
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize, Qt, QUrl, QTimer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QColor, QPalette
from models.configuration import Configuration
from typing import Dict
import logging
from collections import OrderedDict
from models.clips import Clip
import threading
from ffmpeg import probe
from datetime import timedelta
from datetime import datetime
from utils import time_conversions as tc
import GUI.menu_bar as menus
from models.video import Video
from services.exporter import create_video 


logging.getLogger().setLevel(logging.DEBUG)


class Qt_ClipGUI(QMainWindow):
    def __init__(self, conf: Configuration):
        self.conf = conf
        
        super().__init__()
        self.setFixedSize(QSize(1280,840))
        self.setWindowTitle(f"Clip Maker - {conf.projectName}")
        
        
        self.category_dict = {}
        self.init_category_list()
        
        # # FAKE DATA FOR TESTING PURPOSES
        # self.category_dict["offense_erreur"] = [
        #     Clip("00:00:01", "00:00:03"),
        #     Clip("00:02:10", "00:02:15"),
        #     Clip("00:05:30", "00:05:36"),
        #     Clip("00:09:45", "00:09:50"),
        #     Clip("00:14:20", "00:14:27"),
        #     Clip("00:21:05", "00:21:12"),
        #     Clip("00:28:40", "00:28:46"),
        #     Clip("00:36:10", "00:36:18"),
        #     Clip("00:44:55", "00:45:02"),
        #     Clip("00:58:30", "00:58:38"),
        # ]

        # self.category_dict["contre_attaque positif"] = [
        #     Clip("00:00:05", "00:00:08"),
        #     Clip("00:03:20", "00:03:27"),
        #     Clip("00:07:45", "00:07:52"),
        #     Clip("00:12:30", "00:12:36"),
        #     Clip("00:18:10", "00:18:18"),
        #     Clip("00:25:40", "00:25:48"),
        #     Clip("00:33:15", "00:33:22"),
        #     Clip("00:49:50", "00:49:58"),
        # ]
        # ################################
        
        self.main_layout = QHBoxLayout()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setLayout(self.main_layout)
        
        menus.init_menu_bar(self)
        
    
        self.init_video_layout()
        self.init_clip_layout()        
        
        self.current_clip : Clip = None
        
        self.show()

    def init_category_list(self):
        if len(self.conf.preconfiguredCategories) == 0:
            return
        
        for cat in self.conf.preconfiguredCategories:
            self.category_dict[cat] = list()
        

    def init_video_layout(self):
        self.video_widget = QWidget()
        self.video_layout = QVBoxLayout()
        self.video_widget.setLayout(self.video_layout)
        self.main_layout.addWidget(self.video_widget, 7)

        self.video_player_layout = QVBoxLayout()
        self.video_player_widget = QWidget()
        self.video_player_widget.setLayout(self.video_player_layout)
        self.init_video_player()
        self.video_layout.addWidget(self.video_player_widget,7)
        
        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout()
        self.buttons_widget.setLayout(self.buttons_layout)
        
        self.top_button_widget = QWidget()
        self.top_button_layout = QHBoxLayout()
        self.top_button_widget.setLayout(self.top_button_layout)
        self.bottom_button_widget = QWidget()
        self.bottom_button_layout = QHBoxLayout()
        self.bottom_button_widget.setLayout(self.bottom_button_layout)
        
        self.buttons_layout.addWidget(self.top_button_widget)
        self.buttons_layout.addWidget(self.bottom_button_widget)                                
        
        self.init_video_buttons()
        
        self.video_layout.addWidget(self.buttons_widget,1)


    def init_video_player(self):
        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile(self.conf.inputVideo))
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.play()
        self.media_player.setPosition(0)
        self.media_player.pause()        
        self.video_player_layout.addWidget(self.video_widget)
        
        self.video_timeline = QSlider()
        self.video_timeline.setOrientation(Qt.Orientation.Horizontal)
        self.video_timeline.setMaximum(get_video_duration(self.conf.inputVideo))
        
        
        self.video_total_time_ms = str(timedelta(milliseconds=self.video_timeline.maximum())) 
        self.video_hhmmss_lenght = self.video_total_time_ms.split(".")[0]
    
        self.current_time_lbl = QLabel(f"00:00:00 / {self.video_hhmmss_lenght}")

        # Updates the other widget when the video play
        self.media_player.positionChanged.connect(self.change_time_label)
        self.media_player.positionChanged.connect(self.change_video_timeline)
        
        # Handles the moving of the time slider by the user
        self.video_timeline.sliderMoved[int].connect(self.change_video_frame)
        self.video_timeline.valueChanged[int].connect(self.change_video_frame)
            
        self.timeline_layout = QHBoxLayout()
        self.timeline_layout.addWidget(self.current_time_lbl)
        self.timeline_layout.addWidget(self.video_timeline)
        self.video_player_layout.addLayout(self.timeline_layout)
    
    # Instantiate the different buttons we will need to manipulate the video player and
    # create clips from the video
    def init_video_buttons(self):
        self.buttons_dict : Dict[str,QPushButton]  = {}
        
        for button in ["PLAY","PAUSE","START CLIP", "END CLIP", "ADD TO"]:
            new_button = QPushButton(button)
            self.buttons_dict[button] = new_button
            self.top_button_layout.addWidget(new_button)
            
        
        self.video_category_combobox = QComboBox()
        self.update_combobox_values(self.video_category_combobox)
        self.top_button_layout.addWidget(self.video_category_combobox)
        
        for button in ["ADD CATEGORY"]:
            new_button = QPushButton(button)
            self.buttons_dict[button] = new_button
            self.bottom_button_layout.addWidget(new_button,2)
        
        self.bottom_button_layout.setAlignment(self.buttons_dict["ADD CATEGORY"], Qt.AlignmentFlag.AlignRight)
        
        self.connect_actions_buttons()
        self.bind_keystroke()
    
    def connect_actions_buttons(self):
        for key in self.buttons_dict.keys():
            button = self.buttons_dict[key]
            match key:
                case "PLAY":
                    button.clicked.connect(self.start_video)
                    continue
                case "PAUSE": 
                    button.clicked.connect(self.pause_video)
                    continue
                case "START CLIP": 
                    button.clicked.connect(self.start_clipping)
                    continue
                case "END CLIP":
                    button.clicked.connect(self.stop_clipping)
                case "ADD TO": 
                    continue
                case "ADD CATEGORY":
                    button.clicked.connect(self.open_add_category_wdw)
        
    # TODO : Add a configuration option to bind keys to a set of actions (jump forward/backward, start clip, stop clip...)
    def bind_keystroke(self):
        return            
    
    def change_time_label(self,value):        
        hhmmss_time = tc.Timestamp_to_hhmmss(value)
        self.current_time_lbl.setText(f"{hhmmss_time} / {self.video_hhmmss_lenght}")
    
    def change_video_frame(self,value):
        print(f"\n\n value {value}")
        self.media_player.pause()
        self.media_player.setPosition(value)
        self.media_player.play()
    
    def change_video_timeline(self,value):
        self.video_timeline.blockSignals(True)
        self.video_timeline.setSliderPosition(value)
        self.video_timeline.blockSignals(False)
        # setSliderPosition(value) 
    
    def start_clipping(self):
        self.display_fading_message("Starting clipping")
        self.current_clip = Clip(tc.Extract_hhmmss_from_label(self.current_time_lbl), None)

    def display_fading_message(self, message : str, delay : int = 500):
        msg_lbl = QLabel(message, self.top_button_widget)
        msg_lbl.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            color: white;
            padding: 8px;
            border-radius: 6px;
        """)
        msg_lbl.adjustSize()
        QTimer.singleShot(delay, msg_lbl.close)
        msg_lbl.show()
    
    def stop_clipping(self):
        if self.current_clip is None:
            # TODO: add a short message over video that clipping has not started
            return
        current_timestamp = tc.Extract_hhmmss_from_label(self.current_time_lbl)
        if (datetime.strptime(current_timestamp.strip(" "),"%H:%M:%S") - datetime.strptime(self.current_clip.Start,"%H:%M:%S")).total_seconds() <= 0 :
            self.display_fading_message("End of clip is before start", 1200)
            self.current_clip = None
            return
    
        self.current_clip.Add_end(current_timestamp)
        # Add clip to list
        self.add_clip_to_list(self.current_clip)
        # Add preview of clip to clip list layout
        self.current_clip = None

    def add_clip_to_list(self, clip : Clip):
        current_category = self.video_category_combobox.currentText()
        self.category_dict[current_category].append(clip)
        self.update_clip_listbox(current_category)
    
    def update_clip_listbox(self, category: str):
        # Maybe force change of the category 
        if self.clip_category_combobox.currentText() == category:
            self.display_clip_list()
    
    def open_add_category_wdw(self):
        category_name, ok = QInputDialog.getText(self,"Add a category", "Category name")
        if ok and category_name:
            self.category_dict[category_name] = list()
            for combobox in [self.clip_category_combobox,self.video_category_combobox]:
                self.update_combobox_values(combobox)
        
    def init_clip_layout(self):
        self.clip_widget = QWidget()
        self.clip_layout = QVBoxLayout()
        self.clip_widget.setLayout(self.clip_layout)
        
        self.main_layout.addWidget(self.clip_widget, 3)

        self.clip_category_combobox = QComboBox()
        self.update_combobox_values(self.clip_category_combobox)
        self.clip_layout.addWidget(self.clip_category_combobox,2)
        self.clip_category_combobox.currentTextChanged.connect(self.display_clip_list)
        
        self.clip_listbox = QListWidget()
        self.clip_listbox.itemDoubleClicked.connect(self.jump_to_clip)
        self.clip_layout.addWidget(self.clip_listbox, 8)   
    
    def update_combobox_values(self,comb: QComboBox):
        od = OrderedDict(sorted(self.category_dict.items()))
        current_value = comb.currentText()
        comb.clear()
        for cat in od:
            comb.addItem(cat)
        comb.setCurrentText(current_value)
        
    def display_clip_list(self):
        self.clip_listbox.clear()
        for clip in self.category_dict [self.clip_category_combobox.currentText()]:
            new_item = QListWidgetItem(f"{clip.Start}/{clip.End}")
            new_item.setData(1, clip)
            self.clip_listbox.insertItem(0,new_item)
        
    def jump_to_clip(self,item : QListWidgetItem):
        clip = item.data(1)
        timestamp = tc.Hhmmss_to_timestamp(clip.Start)
        self.change_video_frame(timestamp)
    
    def start_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()
        
    def export_project(self):
        logging.debug("Starting export")
        self.export_dict : Dict[str,QLabel] = {}
        self.pause_video()
        # Display a message window
        self.export_wdw = QDialog(self)
        self.export_wdw.setFixedSize(QSize(500,300))
        self.export_wdw.setWindowTitle("Exporting your project")
        self.export_lyt = QVBoxLayout()
        self.export_wdw.setLayout(self.export_lyt)
        message_lbl = QLabel("Exporting...")
        self.export_lyt.addWidget(message_lbl)
        
        self.categories_lyt = QVBoxLayout()
        self.categories_lyt.setContentsMargins(0,1,0,1)
        for cat in self.category_dict.keys():
            if len(self.category_dict[cat]) > 0 :
                self.export_dict[cat] = QLabel(f"... {cat}")
                self.categories_lyt.addWidget(self.export_dict[cat])
        self.export_lyt.addLayout(self.categories_lyt)
        
        self.export_close_btn = QPushButton(text="Close")
        self.export_close_btn.setEnabled(False)
        self.export_close_btn.clicked.connect(self.export_wdw.close)
        self.export_lyt.addWidget(self.export_close_btn)
        self.export_wdw.show()
     
        QTimer.singleShot(0, self.export_video)


    def export_video(self):
          
        for category in self.category_dict.keys():
            logging.debug("Starting creation of video for " + category)
            new_vid = Video(str(category))
            for clip in self.category_dict[category]:
                logging.debug("Adding new clip to video " + category)
                new_vid.AddClip(clip)
            if len(new_vid.Clips) > 0 :
                create_video(output_folder=self.conf.outputDirectory,base_video_path=self.conf.inputVideo,v=new_vid)
                message_lbl = self.export_dict[category]
                message_lbl.setText(f"OK {category}")
                message_lbl.setStyleSheet("QLabel {color : green}")         
        self.export_close_btn.setEnabled(True)
        
        
def get_video_duration(path: str) -> int:
    json_info = probe(path)
    duration_sec = json_info["format"]["duration"]
    duration_ms = float(duration_sec) *1000
    
    return duration_ms.__round__()

