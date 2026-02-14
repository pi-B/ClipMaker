from GUI.setup_gui import SetupGUI
from GUI.welcome_gui import WelcomeGUI
from PyQt6.QtWidgets import QApplication
import logging
import utils.conf_files as conf_utils

logging.getLogger().setLevel(logging.DEBUG)

# TODO : implement resume on crash
# conf = conf_utils.get_conf()

# if conf["running"] != False:
#     last_project = conf["last_projects"][0]

app = QApplication([])
welcome = WelcomeGUI()
welcome.show()
app.exec()
