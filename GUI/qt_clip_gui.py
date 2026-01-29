from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QComboBox, QListWidget, QInputDialog, QSlider, QListWidgetItem, QMenuBar, QDialog
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize, Qt, QUrl, QTimer, pyqtSignal
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtGui import QColor, QPalette
from models.configuration import Configuration
from typing import Dict
import logging
from collections import OrderedDict
from models.clips import Clip
from ffmpeg import probe
from utils import time_conversions as tc
import GUI.menu_bar as menus
from GUI.video_widget import VideoWidget
from GUI.control_widget import ControlWidget
from GUI.clip_widget import ClipWidget
from models.video import Video
from services.exporter import create_video 
from utils.qt_objects import update_combobox_values


logging.getLogger().setLevel(logging.DEBUG)


class Qt_ClipGUI(QMainWindow):
    
    category_dict_changed = pyqtSignal(dict)
    
    def __init__(self, conf: Configuration):
        self.conf = conf
        
        super().__init__()
        self.setFixedSize(QSize(1280,840))
        self.setWindowTitle(f"Clip Maker - {conf.projectName}")
        
        
        self.category_dict = {}
        self.init_category_list()
        self.category_dict_changed.connect(self.update_category_comboboxes)
        
        
        self.main_layout = QHBoxLayout()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setLayout(self.main_layout)
        
        menus.init_menu_bar(self)
        
        self.current_clip : Clip = None
        
        self.video_widget = QWidget()
        self.video_layout = QVBoxLayout()
        self.video_widget.setLayout(self.video_layout)
        self.main_layout.addWidget(self.video_widget, 7)

        
        self.video_player_widget = VideoWidget(self.conf)
        self.video_layout.addLayout(self.video_player_widget.video_player_layout)
        self.video_layout.addWidget(self.video_player_widget,7)
        
        self.clip_widget = ClipWidget(self.category_dict, self.video_widget)
        self.main_layout.addWidget(self.clip_widget, 3)   
        
        self.control_widget = ControlWidget(self.video_player_widget, self.clip_widget, self.category_dict, self.category_dict_changed)
        self.video_layout.addWidget(self.control_widget,1)
       
        # FAKE DATA FOR TESTING PURPOSES
        self.category_dict["offense_erreur"] = [
            Clip("00:00:01", "00:00:03"),
            Clip("00:02:10", "00:02:15"),
            Clip("00:05:30", "00:05:36"),
            Clip("00:09:45", "00:09:50"),
            Clip("00:14:20", "00:14:27"),
            Clip("00:21:05", "00:21:12"),
            Clip("00:28:40", "00:28:46"),
            Clip("00:36:10", "00:36:18"),
            Clip("00:44:55", "00:45:02"),
            Clip("00:58:30", "00:58:38"),
        ]

        self.category_dict["contre_attaque positif"] = [
            Clip("00:00:05", "00:00:08"),
            Clip("00:03:20", "00:03:27"),
            Clip("00:07:45", "00:07:52"),
            Clip("00:12:30", "00:12:36"),
            Clip("00:18:10", "00:18:18"),
            Clip("00:25:40", "00:25:48"),
            Clip("00:33:15", "00:33:22"),
            Clip("00:49:50", "00:49:58"),
        ]
        self.clip_widget.display_clip_list()
        ################################
        
        self.show()

    def update_category_comboboxes(self, values: dict):
        for combobox in [self.control_widget.video_category_combobox, self.clip_widget.clip_category_combobox]:
              combobox = update_combobox_values(values.items(),combobox)

    def init_category_list(self):
        if len(self.conf.preconfiguredCategories) == 0:
            return
        
        for cat in self.conf.preconfiguredCategories:
            self.category_dict[cat] = list()
    
    def update_combobox_values(self,comb: QComboBox):
        od = OrderedDict(sorted(self.category_dict.items()))
        current_value = comb.currentText()
        comb.clear()
        for cat in od:
            comb.addItem(cat)
        comb.setCurrentText(current_value)
        

        
    def jump_to_clip(self,item : QListWidgetItem):
        clip = item.data(1)
        timestamp = tc.Hhmmss_to_timestamp(clip.Start)
        self.change_video_frame(timestamp)
    
        
    def export_project(self):
        logging.debug("Starting export")
        self.export_dict : Dict[str,QLabel] = {}
        self.control_widget.pause_video()
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

