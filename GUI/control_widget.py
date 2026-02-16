from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QComboBox,  QInputDialog
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from typing import Dict
from GUI.video_widget import VideoWidget
from GUI.clip_widget import ClipWidget
from utils import qt_objects
from models.clips import Clip
from utils import time_conversions as tc
from datetime import datetime
from services.auto_saver import AutoSaver

class ControlWidget(QWidget):
    
    def __init__(self, video_widget : VideoWidget, clip_widget : ClipWidget, category_dict : Dict[str,Clip], category_signal : pyqtSignal, auto_saver: AutoSaver):
        super().__init__()
        self.video_widget = video_widget
        self.clip_widget = clip_widget
        self.category_signal = category_signal
        self.category_dict = category_dict
        self.auto_saver = auto_saver
        self.buttons_layout = QVBoxLayout()
        self.setLayout(self.buttons_layout)
        self.top_button_layout = QHBoxLayout()
        self.bottom_button_layout = QHBoxLayout()
        
        self.buttons_dict : Dict[str,QPushButton]  = {}
        
        for button in ["PLAY","PAUSE","START CLIP", "END CLIP", "ADD TO"]:
            new_button = QPushButton(button)
            self.buttons_dict[button] = new_button
            self.top_button_layout.addWidget(new_button)
            
        
        self.video_category_combobox = QComboBox()
        self.video_category_combobox = qt_objects.update_combobox_values(category_dict.items() ,self.video_category_combobox)
        self.top_button_layout.addWidget(self.video_category_combobox)
        
        for button in ["ADD CATEGORY"]:
            new_button = QPushButton(button)
            self.buttons_dict[button] = new_button
            self.bottom_button_layout.addWidget(new_button,2)
        
        self.bottom_button_layout.setAlignment(self.buttons_dict["ADD CATEGORY"], Qt.AlignmentFlag.AlignRight)
        
        self.buttons_layout.addLayout(self.top_button_layout)
        self.buttons_layout.addLayout(self.bottom_button_layout)
        
        self.connect_actions_buttons()
        self.bind_keystroke()
        
        self.current_clip = None
    
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
    
    def start_video(self):
        self.video_widget.media_player.play()


    def pause_video(self):
        self.video_widget.media_player.pause()

    def start_clipping(self):
        if self.video_category_combobox.currentText() == "":
            self.display_fading_message("No category selected")
            return
        self.display_fading_message("Starting clipping")
        self.current_clip = Clip(tc.Extract_hhmmss_from_label(self.video_widget.current_time_lbl), None)

    def display_fading_message(self, message : str, delay : int = 500):
        msg_lbl = QLabel(message, self)
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
        current_timestamp = tc.Extract_hhmmss_from_label(self.video_widget.current_time_lbl)
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
        self.auto_saver.add_clip(current_category,clip)
        self.clip_widget.update_clip_listbox(current_category)
        # In ca

    def open_add_category_wdw(self):
        category_name, ok = QInputDialog.getText(self,"Add a category", "Category name")
        if ok and category_name:
            self.category_dict[category_name] = list()
            self.category_signal.emit(self.category_dict)

    # TODO : Add a configuration option to bind keys to a set of actions (jump forward/backward, start clip, stop clip...)
    def bind_keystroke(self):
        return   