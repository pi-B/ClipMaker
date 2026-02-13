from GUI.setup_gui import SetupGUI
from GUI.welcome_gui import WelcomeGUI
from models.configuration import Configuration
from PyQt6.QtWidgets import QApplication
import logging

logging.getLogger().setLevel(logging.DEBUG)

conf = Configuration()

app = QApplication([])
# setup = SetupGUI(conf)
# setup.show()
welcome = WelcomeGUI()
welcome.show()
app.exec()
