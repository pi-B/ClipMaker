import tkinter as tk
from GUI.clip_gui import ClipGUI 
from GUI.setup_gui import SetupGUI
from models.configuration import Configuration
import logging

logging.getLogger().setLevel(logging.DEBUG)

ready = False
conf = Configuration()

setup = SetupGUI(conf)
setup.mainloop()
if conf.isReady():
    logging.info("Starting main window")
    root = ClipGUI()
    root.mainloop()