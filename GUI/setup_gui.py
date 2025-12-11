import tkinter as tk
from tkinter import Frame,Label, Button, Listbox, Entry, filedialog
from tkinter.ttk import  Combobox
from pathlib import Path
import functools
import logging
from models.configuration import Configuration

def on_focus_entry(event, entry : Entry):
    if entry.cget("background")== "#BE6868":
        entry.config(background = "white") 
    
    return


class SetupGUI(tk.Tk):
    
    def __init__(self, conf : Configuration ):
        super().__init__()
        self.projectConf = conf
        self.geometry("770x540")
        self.title("Setup your project")
        self.resizable(False,False)
        
        self.categoryList = ["toto","tata","lolo","lele"]
        
        self.projectNameLbl = Label(self,text="Project Name")
        self.projectNameLbl.place(x=34,y=31,width=100,height=22)
        
        self.projectNameEntry = Entry(self)
        self.projectNameEntry.place(x=160,y=31,width=430,height=30)
        self.projectNameEntry.bind("<FocusIn>", functools.partial(on_focus_entry, entry=self.projectNameEntry))
        self.projectNameEntry.bind("<FocusOut>", functools.partial(self.on_focus_out_entry_name))
        
        self.videoPathLbl = Label(self,text="Import video")
        self.videoPathLbl.place(x=34,y=92,width=100,height=22)
               
        self.videoPathEntry = Entry(self)
        self.videoPathEntry.place(x=160,y=92,width=430,height=30)
        self.videoPathEntry.bind("<FocusIn>", functools.partial(on_focus_entry, entry=self.videoPathEntry))
        
        self.videoExploreBtn = Button(self, text="Browse", command= self.setFilePathFromBrowser)
        self.videoExploreBtn.place(x=610,y=92,width=60,height=30)
        
        self.outputLbl = Label(self,text="Output path")
        self.outputLbl.place(x=34,y=148,width=95,height=22)
            
        self.outputDirectoryEntry = Entry(self)
        self.outputDirectoryEntry.place(x=160,y=148,width=430,height=30)
        self.outputDirectoryEntry.bind("<FocusIn>", functools.partial(on_focus_entry, entry=self.outputDirectoryEntry))
        
        self.outputDirectoryExploreBtn = Button(self, text="Browse", command= self.setDirectoryPathFromBrowser)
        self.outputDirectoryExploreBtn.place(x=610,y=148,width=60,height=30)
        
        self.categoryListLbl = Label(self, text="Categories")
        self.categoryListLbl.place(x=34,y=205,width=87, height=22)
        
        self.categoryFrame = Frame(self,background="white", border=0.5)
        self.categoryFrame.place(x=34,y=241,width=559,height=278)
        
        self.categoryListbox = Listbox(self,listvariable=self.categoryList)
        self.categoryListbox.place(x=34,y=241,width=559,height=278)
        
        for category in self.categoryList:
            self.categoryListbox.insert(tk.END,category)
                
        self.categoryAddBtn = Button(self, text="Add", command=self.pop_add_category_wdw)
        self.categoryAddBtn.place(x=621,y=241,width=115,height=30)
        
        self.categoryDeleteBtn = Button(self, text="Delete", command=None)
        self.categoryDeleteBtn.place(x=621,y=286,width=115,height=30)
        
        self.startBtn = Button(self, text="Start", command=self.start_project)
        self.startBtn.place(x=621,y=489,width=115,height=30)
        
    def on_focus_out_entry_name(self, event):
        value = self.projectNameEntry.get()
        self.projectConf.projectName = value

        
    def setFilePathFromBrowser(self) :
        filename = filedialog.askopenfilename(initialdir="~",
                                              title="Select a video file",
                                              filetypes=(("Video files","*.mp4"),)
                                            )
        if not Path(filename).exists():
            raise Exception(f"{filename} doesn't seem to exist")
            
        self.videoPathEntry.delete(0, tk.END)
        self.videoPathEntry.insert(0,filename)
        self.projectConf.inputVideo = filename
        
        return
    
    def setDirectoryPathFromBrowser(self):
        directory = filedialog.askdirectory(
            initialdir="~",
            title="Select the output directory",
            mustexist=False
        )
        
        if not Path(directory).exists():
            raise Exception(f"{directory} doesn't seem to exist")

        self.outputDirectoryEntry.delete(0, tk.END)
        self.outputDirectoryEntry.insert(0,directory)
        self.projectConf.outputDirectory = directory
        
        return
        
    def pop_add_category_wdw(self):
        def update_list_category():
            value = self.categoryList.append(inputBox.get())
   
            self.categoryListbox.insert(tk.END,value)
    
            addCategoryWdw.destroy()
    
        addCategoryWdw = tk.Toplevel()
        addCategoryWdw.wm_title("Add new category")
        addCategoryWdw.geometry("245x145")
        
        lab = Label(addCategoryWdw, text="Category", ancho="w")
        lab.place(x=23,y=19,width=117,height=16)
        
        inputBox = tk.Entry(addCategoryWdw)
        inputBox.place(x=23,y=45,width=195,height=40)
        
        addBtn = Button(addCategoryWdw,text="Add",command=update_list_category)
        addBtn.place(x=92,y=95,width=55,height=40)
    
    
    def start_project(self):
        ok = True
        entries : list[Entry] = {self.projectNameEntry, self.videoPathEntry, self.outputDirectoryEntry}
        for entry in entries:
            value = entry.get()
            if len(value) == 0 :
                entry.config(background= "#BE6868")
                ok = False
            
                   
        if not ok :
            return
        else:
            if self.projectConf.projectName == "" and self.projectNameEntry.get() != "":
                self.projectConf.projectName = self.projectNameEntry.get()
            self.destroy()
            
