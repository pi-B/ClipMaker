import logging
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QComboBox, QListWidgetItem, QDialog, QApplication
import json
from pathlib import Path
from models.configuration import Configuration
from GUI.qt_clip_gui import Qt_ClipGUI
import utils.conf_files as conf_utils 

class WelcomeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(420,250)
        self.setWindowTitle("Clip Maker")
        
        self.app_conf = conf_utils.get_conf()
                   
        self.conf_dict = {}
        
        self.main_layout = QVBoxLayout()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central.setLayout(self.main_layout)
        
        self.existing_project_combobox = QComboBox()
        # self.existing_project_combobox.setContentsMargins(100,0,100,0)
        self.resume_project_btn = QPushButton(text="Resume project")
        self.new_project_btn = QPushButton(text="New project")
        
        self.main_layout.addWidget(self.existing_project_combobox)
        self.main_layout.addWidget(self.resume_project_btn)
        self.main_layout.addWidget(self.new_project_btn)
        
        for projects_path in self.app_conf["last_projects"]:
            logging.debug(projects_path)
            if Path(projects_path + "/.project/auto_save.json").exists() :
                with open(projects_path + "/.project/auto_save.json", "r") as file:
                    auto_save_data = json.loads(file.read())
                    file.close()
                if auto_save_data is not None :
                    logging.debug(auto_save_data["project_name"])
                    # Use the value in user data to retrieve the project's directory
                    self.existing_project_combobox.addItem(auto_save_data["project_name"],{"output_directory": projects_path, "input_video":auto_save_data["input_video"]})
                    
        self.resume_project_btn.clicked.connect(self.resume_project)
        self.new_project_btn.clicked.connect(self.start_new_project)
        
    def resume_project(self):
        conf = Configuration()
        conf.projectName = self.existing_project_combobox.currentText()
        conf.outputDirectory = self.existing_project_combobox.currentData()["output_directory"]
        conf.inputVideo = self.existing_project_combobox.currentData()["input_video"]

        self.app_conf["last_projects"] = conf_utils.add_current_project(self.app_conf["last_projects"], self.existing_project_combobox.currentData()["output_directory"])
        conf_utils.update_conf_file(self.app_conf)
            
        self.main = Qt_ClipGUI(conf)
        self.close()
        self.main.show()
    
    def start_new_project(self):
        pass
                