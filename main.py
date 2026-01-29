import tkinter as tk
from GUI.setup_gui import SetupGUI
from GUI.qt_clip_gui import Qt_ClipGUI
from models.configuration import Configuration
from PyQt6.QtWidgets import QApplication
import logging

logging.getLogger().setLevel(logging.DEBUG)

ready = False
conf = Configuration()

# setup = SetupGUI(conf)
# setup.mainloop()

conf.inputVideo = "/Users/macos/clip_maker/outputs/LEZAT_EXTER/lezat_tcms.mp4"
conf.outputDirectory = "/Users/macos/clip_maker/outputs/LEZAT_EXTER2/"
conf.projectName = "lezat_exter"
conf.preconfiguredCategories = ["offense_erreur", "offense positif", "defense_negatof","defense-positif", "contre_attaque positif"]

if conf.isReady():
    logging.info("Starting main window")
    app = QApplication([])
    root = Qt_ClipGUI(conf)
    app.exec()
