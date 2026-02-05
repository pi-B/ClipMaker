from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QComboBox, QListWidget, QInputDialog, QSlider, QListWidgetItem, QMenuBar, QDialog
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget
from typing import Dict
from models.clips import Clip
from utils import qt_objects
from utils import time_conversions as tc
from GUI.video_widget import VideoWidget

class ClipWidget(QWidget):
    
    def __init__(self, category_dict : Dict[str,Clip], video_widget: VideoWidget):
        super().__init__()
        self.category_dict = category_dict
        self.video_widget = video_widget
        self.clip_layout = QVBoxLayout()
        self.setLayout(self.clip_layout)
        
        self.clip_category_combobox = QComboBox()
        self.clip_category_combobox = qt_objects.update_combobox_values(category_dict.items(), self.clip_category_combobox)
        self.clip_category_combobox.currentTextChanged.connect(self.display_clip_list)
        self.clip_layout.addWidget(self.clip_category_combobox,2)
        
        self.clip_listbox = QListWidget()
        self.clip_listbox.itemDoubleClicked.connect(self.jump_to_clip)
        self.clip_layout.addWidget(self.clip_listbox, 8)
        
        for cat in self.category_dict.keys():
            self.display_clip_list(cat)
            break 
        
    def display_clip_list(self, value : str):
        self.clip_listbox.clear()
        if value == "":
            return
        for clip in self.category_dict[value]:
            new_item = QListWidgetItem(f"{clip.Start}/{clip.End}")
            new_item.setData(1, clip)
            self.clip_listbox.insertItem(0,new_item)
            
    def jump_to_clip(self,item : QListWidgetItem):
        clip = item.data(1)
        timestamp = tc.Hhmmss_to_timestamp(clip.Start)
        self.video_widget.change_video_frame(timestamp)
        
    def update_clip_listbox(self, category: str):
        # Maybe force change of the category 
        if self.clip_category_combobox.currentText() == category:
            self.display_clip_list()