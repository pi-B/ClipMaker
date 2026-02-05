import tkinter as tk
from GUI.setup_gui import SetupGUI
from models.configuration import Configuration
from PyQt6.QtWidgets import QApplication
import logging

logging.getLogger().setLevel(logging.DEBUG)

ready = False
conf = Configuration()

app = QApplication([])
setup = SetupGUI(conf)
setup.show()
app.exec()
