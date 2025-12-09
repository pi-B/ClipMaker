import tkinter as tk
from tkinter import Frame,Label, Button, Listbox
from tkinter.ttk import  Combobox 
import logging

logging.getLogger().setLevel(logging.DEBUG)

class ClipGUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry("1280x840")
        self.videoFrame = Frame(self, background="#BE6868")
        self.videoFrame.place(x=0,y=45,width=928,height=800)
        
        self.clipFrame = Frame(self, background="#174498")
        self.clipFrame.place(x=927,y=45,width=357,height=800)
        
        self.categoryList = []
        
        self.init_video_frame()
        self.init_clip_frame()
    
    def init_video_frame(self):
        
        self.fakeVideoPlayer = Frame(self.videoFrame, background="black")
        self.fakeVideoPlayer.place(x=29,y=7,width=890,height=500)
        
        self.playBtn = Button(self.videoFrame, background="#ADAAAA", text="Play")
        self.playBtn.place(x=28,y=574,width=100,height=40)
        
        self.pauseBtn= Button(self.videoFrame, background="#ADAAAA", text="Pause")
        self.pauseBtn.place(x=157,y=574,width=100,height=40)
        
        self.startClipBtn= Button(self.videoFrame, background="#ADAAAA", text="Start clip")
        self.startClipBtn.place(x=285,y=574,width=100,height=40)
        
        self.endClipBtn= Button(self.videoFrame, background="#ADAAAA", text="End clip")
        self.endClipBtn.place(x=413,y=574,width=100,height=40)
        
        self.addClipBtn = Button(self.videoFrame, background="#ADAAAA", text="Add to")
        self.addClipBtn.place(x=541,y=574,width=100,height=40)
        
        self.categoryComboboxVideo = Combobox(self.videoFrame, background="#ADAAAA", values=self.categoryList)
        self.categoryComboboxVideo.place(x=669,y=581,width=238,height=30)
        
        self.addCategoryBtn = Button(self.videoFrame, background="#ADAAAA", text="Add category", command=self.pop_add_category_wdw)
        self.addCategoryBtn.place(x=670,y=670,width=238,height=40)
        
        # .place(x=,y=,width=,height=)
        # .place(x=,y=,width=,height=)
        # .place(x=,y=,width=,height=)
        
    def init_clip_frame(self):
        self.categoryComboboxClip = Combobox(self.clipFrame, values=self.categoryList)
        self.categoryComboboxClip.place(x=14,y=12,width=238,height=30)
        
        self.listClips = Listbox(self.clipFrame)
        self.listClips.place(x=14,y=61,width=324,height=724)
        
    
    def pop_add_category_wdw(self):
        def update_list_category():
            self.categoryList.append(inputBox.get())
            self.categoryList.sort()
            self.categoryComboboxVideo["values"] = self.categoryList
            self.categoryComboboxClip["values"] = self.categoryList
            
            logging.debug(f"values in the category list {self.categoryList} ")
            
            if len(self.categoryList) == 1 :
                self.categoryComboboxClip.set(self.categoryList[0])
                self.categoryComboboxVideo.set(self.categoryList[0])
            
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
        