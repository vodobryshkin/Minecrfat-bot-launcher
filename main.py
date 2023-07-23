import sys
import sqlite3

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem

from qt_designes.qtmainlauncher import Ui_MainWindow
from qt_designes.qtcreatebot import Ui_CreateForm

base = sqlite3.connect('pixbot.db')
cur = base.cursor()

base.execute(
    'CREATE TABLE IF NOT EXISTS bots (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL'
    ', server TEXT NOT NULL, version TEXT NOT NULL)')


class CreateForm(QWidget, Ui_CreateForm):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)

        self.parent = parent


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = MainLauncher()
    launcher.show()
    sys.exit(app.exec())
