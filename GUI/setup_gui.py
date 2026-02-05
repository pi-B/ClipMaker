import tkinter as tk
from tkinter import Frame,Label, Button, Listbox, Entry, filedialog
from tkinter.ttk import  Combobox
from pathlib import Path
import functools
import logging
from models.configuration import Configuration
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QComboBox, QListWidget, QInputDialog, QSlider, QListWidgetItem, QMenuBar, QDialog, QFileDialog, QLineEdit, QFormLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QDir, Qt, QFile
from GUI.qt_clip_gui import Qt_ClipGUI



def on_focus_entry(event, entry : Entry):
    if entry.cget("background")== "#BE6868":
        entry.config(background = "white") 
    
    return

class SetupGUI(QWidget):
    def __init__(self, conf: Configuration):
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
        # form_lyt.setHorizontalSpacing(10)
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
            self.projectConf.outputDirectory    = self.source_video_path.text() 
            
            self.main_window = Qt_ClipGUI(self.projectConf)  
            self.main_window.show() 
            self.close()
        
        
        
# class SetupGUI(tk.Tk):
    
#     def __init__(self, conf : Configuration ):
#         super().__init__()
#         self.projectConf = conf
#         self.geometry("770x540")
#         self.title("Setup your project")
#         self.resizable(False,False)
        
#         self.categoryList = []
        
#         self.projectNameLbl = Label(self,text="Project Name")
#         self.projectNameLbl.place(x=34,y=31,width=100,height=22)
        
#         self.projectNameEntry = Entry(self)
#         self.projectNameEntry.place(x=160,y=31,width=430,height=30)
#         self.projectNameEntry.bind("<FocusIn>", functools.partial(on_focus_entry, entry=self.projectNameEntry))
#         self.projectNameEntry.bind("<FocusOut>", functools.partial(self.on_focus_out_entry_name))
        
#         self.videoPathLbl = Label(self,text="Import video")
#         self.videoPathLbl.place(x=34,y=92,width=100,height=22)
               
#         self.videoPathEntry = Entry(self)
#         self.videoPathEntry.place(x=160,y=92,width=430,height=30)
#         self.videoPathEntry.bind("<FocusIn>", functools.partial(on_focus_entry, entry=self.videoPathEntry))
        
#         self.videoExploreBtn = Button(self, text="Browse", command= self.setFilePathFromBrowser)
#         self.videoExploreBtn.place(x=610,y=92,width=60,height=30)
        
#         self.outputLbl = Label(self,text="Output path")
#         self.outputLbl.place(x=34,y=148,width=95,height=22)
            
#         self.outputDirectoryEntry = Entry(self)
#         self.outputDirectoryEntry.place(x=160,y=148,width=430,height=30)
#         self.outputDirectoryEntry.bind("<FocusIn>", functools.partial(on_focus_entry, entry=self.outputDirectoryEntry))
        
#         self.outputDirectoryExploreBtn = Button(self, text="Browse", command= self.setDirectoryPathFromBrowser)
#         self.outputDirectoryExploreBtn.place(x=610,y=148,width=60,height=30)
        
#         self.categoryListLbl = Label(self, text="Categories")
#         self.categoryListLbl.place(x=34,y=205,width=87, height=22)
        
#         self.categoryFrame = Frame(self,background="white", border=0.5)
#         self.categoryFrame.place(x=34,y=241,width=559,height=278)
        
#         self.categoryListbox = Listbox(self,listvariable=self.categoryList)
#         self.categoryListbox.place(x=34,y=241,width=559,height=278)
        
#         for category in self.categoryList:
#             self.categoryListbox.insert(tk.END,category)
                
#         self.categoryAddBtn = Button(self, text="Add", command=self.pop_add_category_wdw)
#         self.categoryAddBtn.place(x=621,y=241,width=115,height=30)
        
#         self.categoryDeleteBtn = Button(self, text="Delete", command=None)
#         self.categoryDeleteBtn.place(x=621,y=286,width=115,height=30)
        
#         self.startBtn = Button(self, text="Start", command=self.start_project)
#         self.startBtn.place(x=621,y=489,width=115,height=30)
        
#     def on_focus_out_entry_name(self, event):
#         value = self.projectNameEntry.get()
#         self.projectConf.projectName = value

        
#     def setFilePathFromBrowser(self) :
#         filename = filedialog.askopenfilename(initialdir="~",
#                                               title="Select a video file",
#                                               filetypes=(("Video files","*.mp4"),)
#                                             )
#         if not Path(filename).exists():
#             raise Exception(f"{filename} doesn't seem to exist")
            
#         self.videoPathEntry.delete(0, tk.END)
#         self.videoPathEntry.insert(0,filename)
#         self.projectConf.inputVideo = filename
        
#         return
    
#     def setDirectoryPathFromBrowser(self):
#         directory = filedialog.askdirectory(
#             initialdir="~",
#             title="Select the output directory",
#             mustexist=False
#         )
        
#         if not Path(directory).exists():
#             raise Exception(f"{directory} doesn't seem to exist")

#         self.outputDirectoryEntry.delete(0, tk.END)
#         self.outputDirectoryEntry.insert(0,directory)
#         self.projectConf.outputDirectory = directory
        
#         return
        
#     def pop_add_category_wdw(self):
#         def update_list_category():
#             value = self.categoryList.append(inputBox.get())
   
#             self.categoryListbox.insert(tk.END,value)
    
#             addCategoryWdw.destroy()
    
#         addCategoryWdw = tk.Toplevel()
#         addCategoryWdw
#         addCategoryWdw.wm_title("Add new category")
#         addCategoryWdw.geometry("245x145")
        
#         lab = Label(addCategoryWdw, text="Category", ancho="w")
#         lab.place(x=23,y=19,width=117,height=16)
        
#         inputBox = tk.Entry(addCategoryWdw)
#         inputBox.place(x=23,y=45,width=195,height=40)
        
#         addBtn = Button(addCategoryWdw,text="Add",command=update_list_category)
#         addBtn.place(x=92,y=95,width=55,height=40)
    
    
#     def start_project(self):
#         ok = True
#         entries : list[Entry] = {self.projectNameEntry, self.videoPathEntry, self.outputDirectoryEntry}
#         for entry in entries:
#             value = entry.get()
#             if len(value) == 0 :
#                 entry.config(background= "#BE6868")
#                 ok = False
            
                   
#         if not ok :
#             return
#         else:
#             if self.projectConf.projectName == "" and self.projectNameEntry.get() != "":
#                 self.projectConf.projectName = self.projectNameEntry.get()
#             self.destroy()
            
