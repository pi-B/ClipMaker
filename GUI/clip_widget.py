from PyQt6.QtWidgets import QVBoxLayout,  QWidget,  QComboBox, QListWidget,   QListWidgetItem, QMenu
from PyQt6.QtCore import Qt, QPoint
from typing import Dict
from models.clips import Clip
from services.auto_saver import AutoSaver
from utils import qt_objects
from utils import time_conversions as tc
from GUI.video_widget import VideoWidget
from typing import List

class ClipWidget(QWidget):
    
    def __init__(self, category_dict : Dict[str,List[Clip]], video_widget: VideoWidget, auto_saver : AutoSaver):
        super().__init__()
        self.auto_saver = auto_saver
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
        self.clip_listbox.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.clip_listbox.customContextMenuRequested.connect(lambda pos: self.show_clip_menu(self.clip_listbox, pos))
        self.clip_layout.addWidget(self.clip_listbox, 8)
        
        for cat in self.category_dict.keys():
            self.display_clip_list(cat)
            break 
    
    def show_clip_menu(self, listwidget: QListWidget, position : QPoint):
        selected_clip = listwidget.itemAt(position)
        if selected_clip is not None:
            menu = QMenu()
            action = menu.addAction("Supprimer")
            action.triggered.connect(lambda: self.delete_clip(selected_clip))
            menu.exec(listwidget.viewport().mapToGlobal(position))
    
    def delete_clip(self, clip_item: QListWidgetItem) :
        category = self.clip_category_combobox.currentText()
        remove_clip = clip_item.data(1)
        self.clip_listbox.takeItem(self.clip_listbox.row(clip_item))
        
        if self.category_dict.get(category) is not None :
            for i in range(0,len(self.category_dict[category])):
                clip = self.category_dict[category][i]
                if clip.Start == remove_clip.Start and clip.End == remove_clip.End:
                    self.category_dict[category].pop(i)
                    break
        
        self.auto_saver.remove_clip(category, remove_clip)
        
        
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
            self.display_clip_list(category)