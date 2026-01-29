import tkinter as tk
from tkinter import Frame,Label, Button, Listbox, StringVar, Canvas
from tkinter.ttk import  Combobox 
import logging
from models.configuration import Configuration
import vlc
import sys

logging.getLogger().setLevel(logging.DEBUG)

class ClipGUI(tk.Tk):
    
    def __init__(self, conf: Configuration):
        super().__init__()
        self.conf = conf
        self.geometry("1280x840")
        self.title(f"Clip Maker - {conf.projectName}")
        self.videoFrame = Frame(self, background="#BE6868")
        self.videoFrame.place(x=0,y=45,width=928,height=800)
        
        self.clipFrame = Frame(self)
        self.clipFrame.place(x=927,y=45,width=357,height=800)
        
        self.categoryList = []
        self.init_category_list()        
        self.firstCategoryValue = StringVar()
        
        self.init_video_frame()
        self.init_clip_frame()
        
        if len(self.categoryList) != 0:
            self.firstCategoryValue.set(self.categoryList[0])

        self.init_video_player()
        
    def init_category_list(self):
        if len(self.conf.preconfiguredCategories) == 0:
            return
        
        for cat in self.conf.preconfiguredCategories:
            self.categoryList.append(cat)
        
        self.categoryList.sort()
    
    def init_video_frame(self):
        
        # self.fakeVideoPlayer = Frame(self.videoFrame)
        # self.fakeVideoPlayer.place(x=29,y=7,width=890,height=500)
        self.videoCanvas = Canvas(self.videoFrame)
        self.videoCanvas.place(x=29,y=7,width=890,height=500)
        
        self.playBtn = Button(self.videoFrame, background="#ADAAAA", text="Play",command=self.start_video)
        self.playBtn.place(x=28,y=574,width=100,height=40, )
        
        self.pauseBtn= Button(self.videoFrame, background="#ADAAAA", text="Pause")
        self.pauseBtn.place(x=157,y=574,width=100,height=40)
        
        self.startClipBtn= Button(self.videoFrame, background="#ADAAAA", text="Start clip")
        self.startClipBtn.place(x=285,y=574,width=100,height=40)
        
        self.endClipBtn= Button(self.videoFrame, background="#ADAAAA", text="End clip")
        self.endClipBtn.place(x=413,y=574,width=100,height=40)
        
        self.addClipBtn = Button(self.videoFrame, background="#ADAAAA", text="Add to")
        self.addClipBtn.place(x=541,y=574,width=100,height=40)
        
        self.categoryComboboxVideo = Combobox(self.videoFrame, background="#ADAAAA", values=self.categoryList, textvariable=self.firstCategoryValue)
        self.categoryComboboxVideo.place(x=669,y=581,width=238,height=30)
        
        self.addCategoryBtn = Button(self.videoFrame, background="#ADAAAA", text="Add category", command=self.pop_add_category_wdw)
        self.addCategoryBtn.place(x=670,y=670,width=238,height=40)
        
        
    def init_clip_frame(self):
        self.categoryComboboxClip = Combobox(self.clipFrame, values=self.categoryList, textvariable=self.firstCategoryValue)
        self.categoryComboboxClip.place(x=14,y=12,width=238,height=30)
        
        self.listClips = Listbox(self.clipFrame)
        self.listClips.place(x=14,y=61,width=324,height=724)
        
    def init_video_player(self):
        self.player_instance = vlc.Instance("--vout=opengl")
        self.player = self.player_instance.media_player_new() 
        
        logging.debug(f"Setting media new path as : {self.conf.inputVideo}")
        self.video = self.player_instance.media_new(self.conf.inputVideo)
        self.player.set_media(self.video)
        
        self.update_idletasks()
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.videoCanvas.winfo_id())
        elif sys.platform == "win32":
            self.player.set_hwnd(self.videoCanvas.winfo_id())
        elif sys.platform == "darwin":
            self.player.set_nsobject(self.videoCanvas.winfo_id())
        
        
        
    def start_video(self):
        try:
            self.player.play()
        except Exception as e:
            logging.error(f"{e=}")
        # self.player.video_set_deinterlace()
            
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
    
