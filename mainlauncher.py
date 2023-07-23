import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox

from py_designes.qtmainlauncher import Ui_MainWindow

from exceptions import VersionError, ExistingBotError
from tools import check_existing_bot, check_version
from bot import MineBot

base = sqlite3.connect('pixbot.db')
cur = base.cursor()

base.execute('CREATE TABLE IF NOT EXISTS bots (name TEXT NOT NULL, server TEXT NOT NULL, version TEXT NOT NULL)')
base.execute('CREATE TABLE IF NOT EXISTS running (name TEXT NOT NULL, server TEXT NOT NULL)')


class MainLauncher(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.create_bot_button.clicked.connect(self.create_bot_method)
        self.delete_bot_button.clicked.connect(self.delete_bot_method)
        self.run_bot_button.clicked.connect(self.run_bot_method)
        self.stop_bot_button.clicked.connect(self.stop_bot_method)

        self.run_bot_combobox.activated.connect(self.run_handleActivated)
        self.delete_bot_combobox.activated.connect(self.delete_handleActivated)
        self.stop_bot_combobox.activated.connect(self.stop_handleActivated)

        self.run_bot_combobox_list = [f'{elem[0]}-{elem[1]}' for elem in
                                      cur.execute('''SELECT name, server FROM bots''').fetchall()]

        self.stop_bot_combobox_list = []

        try:
            self.chosen_run_bot_combobox = self.run_bot_combobox_list[0]
        except IndexError:
            self.chosen_run_bot_combobox = ''

        try:
            self.chosen_delete_bot_combobox = self.run_bot_combobox_list[0]
        except IndexError:
            self.chosen_delete_bot_combobox = ''

        self.chosen_stop_bot_combobox = ''

        self.run_bot_combobox.addItems(self.run_bot_combobox_list)
        self.delete_bot_combobox.addItems(self.run_bot_combobox_list)
        self.stop_bot_combobox.addItems(self.stop_bot_combobox_list)

        self.running_bots_list = []

        self.table_update()

    def run_handleActivated(self, index):
        self.chosen_run_bot_combobox = self.run_bot_combobox.itemText(index)

    def stop_handleActivated(self, index):
        self.chosen_stop_bot_combobox = self.stop_bot_combobox.itemText(index)

    def delete_handleActivated(self, index):
        self.chosen_delete_bot_combobox = self.delete_bot_combobox.itemText(index)

    def create_bot_method(self):
        try:
            if check_existing_bot(self.name_edit.text(), self.server_edit.text()):
                raise ExistingBotError
            if check_version(self.version_edit.text()):
                raise VersionError

            cur.execute("""INSERT INTO bots VALUES (?, ?, ?)""", (self.name_edit.text(), self.server_edit.text(),
                                                              self.version_edit.text()))
            base.commit()

            self.table_update()
            self.error_label.setText('')

            self.run_bot_combobox_list.append(f'{self.name_edit.text()}-{self.server_edit.text()}')

            if len(self.run_bot_combobox_list) == 1:
                self.chosen_delete_bot_combobox = self.run_bot_combobox_list[0]
                self.chosen_run_bot_combobox = self.run_bot_combobox_list[0]

            self.run_bot_combobox.clear()
            self.run_bot_combobox.addItems(self.run_bot_combobox_list)
            self.delete_bot_combobox.clear()
            self.delete_bot_combobox.addItems(self.run_bot_combobox_list)

        except VersionError:
            self.error_label.setText('<h1 style="color: rgb(250, 55, 55);">Такой версии нет.</h1>')

        except ExistingBotError:
            self.error_label.setText('<h1 style="color: rgb(250, 55, 55);">Такой бот уже есть.</h1>')

    def delete_bot_method(self):
        try:
            name, server = self.chosen_delete_bot_combobox.split('-')[0], self.chosen_delete_bot_combobox.split('-')[1]

            cur.execute(f"""DELETE FROM bots WHERE name='{name}' AND server='{server}'""")
            base.commit()
            self.table_update()

            del self.run_bot_combobox_list[self.run_bot_combobox_list.index(self.chosen_delete_bot_combobox)]

            self.run_bot_combobox.clear()
            self.run_bot_combobox.addItems(self.run_bot_combobox_list)
            self.delete_bot_combobox.clear()
            self.delete_bot_combobox.addItems(self.run_bot_combobox_list)

            try:
                self.chosen_delete_bot_combobox = self.run_bot_combobox_list[0]
            except IndexError:
                self.chosen_delete_bot_combobox = ''
                self.chosen_run_bot_combobox = ''

            self.error_label.setText('')

        except Exception as err:
            self.error_label.setText('<h1 style="color: rgb(250, 55, 55);">Бота нет.</h1>')

    def run_bot_method(self):
        try:
            name, server = self.chosen_run_bot_combobox.split('-')

            res = cur.execute((f"""SELECT * FROM bots WHERE name= '{name}' AND server='{server}'""")).fetchall()[0]

            name, server, version = res

            self.running_bots_list.append(MineBot(name, server, version))
            self.running_bots_list[-1].run()

            self.stop_bot_combobox_list.append(f'{name}-{server}')

            if len(self.stop_bot_combobox_list) == 1:
                self.chosen_stop_bot_combobox = f'{name}-{server}'

            ind = -1
            for i in range(len(self.run_bot_combobox_list)):
                n_name, n_server = self.run_bot_combobox_list[i].split('-')
                if n_name == name and n_server == server:
                    ind = i
                    break

            del self.run_bot_combobox_list[ind]

            self.run_bot_combobox.clear()
            self.run_bot_combobox.addItems(self.run_bot_combobox_list)

            self.chosen_run_bot_combobox = self.run_bot_combobox_list[0]

            self.stop_bot_combobox.clear()
            self.stop_bot_combobox.addItems(self.stop_bot_combobox_list)

            cur.execute('''INSERT INTO running VALUES (?, ?)''', (name, server))
            base.commit()

        except Exception as err:
            print(type(err), err)
            self.error_label.setText('<h1 style="color: rgb(250, 55, 55);">Бота нет.</h1>')

    def stop_bot_method(self):
        try:
            name, server = self.chosen_stop_bot_combobox.split('-')

            cur.execute((f"""DELETE FROM running WHERE name='{name}' AND server='{server}'"""))
            base.commit()

            ind = -1
            for i in range(len(self.running_bots_list)):
                if self.running_bots_list[i].username == name and self.running_bots_list[i].server == server:
                    ind = i
                    break

            del self.running_bots_list[ind]

            ind = -1
            for i in range(len(self.stop_bot_combobox_list)):
                n_name, n_server = self.stop_bot_combobox_list[i].split('-')

                if n_name == name and n_server == server:
                    ind = i
                    break

            del self.stop_bot_combobox_list[ind]

            self.stop_bot_combobox.clear()
            self.stop_bot_combobox.addItems(self.stop_bot_combobox_list)

        except Exception as err:
            print(type(err), err)
            self.error_label.setText('<h1 style="color: rgb(250, 55, 55);">Бота нет.</h1>')

    def table_update(self):
        query = "SELECT * FROM bots"
        res = cur.execute(query).fetchall()

        self.bot_tablewidjet.setColumnCount(3)
        self.bot_tablewidjet.setHorizontalHeaderLabels(['Имя', 'Сервер', 'Версия'])
        self.bot_tablewidjet.setRowCount(0)

        for i, row in enumerate(res):
            self.bot_tablewidjet.setRowCount(self.bot_tablewidjet.rowCount() + 1)

            for j, elem in enumerate(row):
                self.bot_tablewidjet.setItem(i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Вопрос', 'Точно хотите закрыть?',
            QMessageBox.Yes, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            for i in range(len(self.running_bots_list)):
                self.running_bots_list[i].stop()
            event.accept()
        else:
            event.ignore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = MainLauncher()
    launcher.show()
    sys.except_hook = except_hook
    sys.exit(app.exec())
