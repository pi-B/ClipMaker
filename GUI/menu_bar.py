from PyQt6.QtWidgets import QMainWindow, QMenu

def init_menu_bar(root : QMainWindow):
    menu = root.menuBar()
    file_menu = menu.addMenu("File")
    init_file_menu(root, file_menu)
    menu.addMenu(file_menu)
    root.setMenuBar(menu)
    
def init_file_menu(root: QMainWindow, file_menu : QMenu):
    file_menu.addAction("New project")
    export_button = file_menu.addAction("Export")
    export_button.triggered.connect(root.export_project)
        

    