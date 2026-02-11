from pathlib import Path
import logging
from models.configuration import Configuration
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton,  QListWidget, QInputDialog, QFileDialog, QLineEdit, QFormLayout
from PyQt6.QtCore import QDir, Qt
from GUI.qt_clip_gui import Qt_ClipGUI
from services.auto_saver import AutoSaver

class SetupGUI(QWidget):
    def __init__(self, conf: Configuration):
        # auto_saver = AutoSaver() # test if the 

        super().__init__()
        self.projectConf = conf
        self.setFixedSize(770,540)
        self.setWindowTitle("Setup your project")
        self.categoryList = []
        
        setup_layout = QVBoxLayout()
        self.setLayout(setup_layout)
        
        form_lyt = QFormLayout()
        form_lyt.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_lyt.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_lyt.setVerticalSpacing(8)
        form_lyt.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        
        
        self.input_project_name = QLineEdit(self)
        form_lyt.addRow("Project name", self.input_project_name)
        
        source_video_lyt = QHBoxLayout()
        self.source_video_path = QLineEdit(self)
        self.search_source_video_btn = QPushButton(self)
        self.search_source_video_btn.setText("browse")
        self.search_source_video_btn.clicked.connect(self.set_video_path)
        source_video_lyt.addWidget(self.source_video_path)
        source_video_lyt.addWidget(self.search_source_video_btn)
        form_lyt.addRow("Import video", source_video_lyt)
                
        output_directory_lyt = QHBoxLayout()
        self.output_directory_path = QLineEdit(self)
        self.search_output_directory_btn = QPushButton(self)
        self.search_output_directory_btn.setText("browse")
        self.search_output_directory_btn.clicked.connect(self.set_output_path)
        output_directory_lyt.addWidget(self.output_directory_path)
        output_directory_lyt.addWidget(self.search_output_directory_btn)
        form_lyt.addRow("Output directory", output_directory_lyt)
                   
        categories_lyt = QVBoxLayout()
        category_widgets_lyt = QHBoxLayout()
        category_buttons_lyt = QVBoxLayout()
        self.output_directory_lbl = QLabel(self,text="Categories")
        categories_lyt.addWidget(self.output_directory_lbl)
        self.categories_list = QListWidget()
        category_widgets_lyt.addWidget(self.categories_list,8)
        
        self.add_category_btn = QPushButton(text="Add")
        self.add_category_btn.clicked.connect(self.add_category)
        self.delete_category_btn = QPushButton(text="Delete")       
        self.delete_category_btn.clicked.connect(self.remove_selection)
        self.start_project_btn = QPushButton(text="Start")
        self.start_project_btn.clicked.connect(self.start_project)
        category_buttons_lyt.addWidget(self.add_category_btn, alignment= Qt.AlignmentFlag.AlignTop)
        category_buttons_lyt.addSpacing(5)
        category_buttons_lyt.addWidget(self.delete_category_btn, alignment= Qt.AlignmentFlag.AlignTop)
        category_buttons_lyt.addStretch()
        category_buttons_lyt.addWidget(self.start_project_btn, alignment= Qt.AlignmentFlag.AlignBottom)

        category_widgets_lyt.addLayout(category_buttons_lyt,2)
        categories_lyt.addLayout(category_widgets_lyt)
        setup_layout.addLayout(form_lyt)
        setup_layout.addLayout(categories_lyt)
        
        setup_layout.setContentsMargins(40,5,40,5)
        
        self.input_project_name.setText("test")
        self.source_video_path.setText("/Users/macos/entrainement2.mp4")
        self.output_directory_path.setText("/Users/macos/")
        
        self.show()
        
    
    def set_video_path(self):
        self.file_explorer = QFileDialog(self)
        video_path = self.file_explorer.getOpenFileName(self, caption="Choose the video you want to clip from", directory= QDir.currentPath(), filter="Video (*.mp4 *.wav)")
        if len(video_path[0]) != 0:
            self.source_video_path.setText(video_path[0])
    
    def set_output_path(self):
        self.file_explorer = QFileDialog(self)
        output_path = self.file_explorer.getExistingDirectory(self, caption="Choose the directory to output the final videos to",directory=QDir.currentPath())
        if len(output_path) != 0:
            self.output_directory_path.setText(output_path)
        
    def add_category(self):
        category_name, ok = QInputDialog.getText(self,"Add a category", "Category", flags=Qt.WindowType.WindowStaysOnTopHint)
        if ok and category_name:
            self.categories_list.addItem(category_name)

    def remove_selection(self):
        listItems = self.categories_list.selectedItems()
        if listItems is None : 
            logging.debug("empty list")
            return
        for item in listItems:
            self.categories_list.takeItem(self.categories_list.row(item))
    
    def start_project(self):
        ok = True
        if self.input_project_name.text() == "":
            ok = False
            self.input_project_name.setStyleSheet("""
                    QLineEdit {
                        background-color: #ffcccc;
                        border: 1px solid red;
                    }
                """)
        else :
            self.input_project_name.setStyleSheet("""
                    QLineEdit {
                    }
                """)
        
        for entry in [self.source_video_path, self.output_directory_path]:
            if entry.text() == "" or not Path(entry.text()).exists():
                ok = False
                entry.setStyleSheet("""
                        QLineEdit {
                            background-color: #ffcccc;
                            border: 1px solid red;
                        }
                    """)
            else :
                entry.setStyleSheet("""
                        QLineEdit {
                        }
                    """)
            
        if not ok :
            return
        else:
            logging.debug("finalizing")
            self.projectConf.projectName        = self.input_project_name.text()
            self.projectConf.inputVideo         = self.source_video_path.text()
            self.projectConf.outputDirectory    = self.output_directory_path.text() 
            
            self.main_window = Qt_ClipGUI(self.projectConf)  
            self.main_window.show() 
            self.close()
        
        
        
