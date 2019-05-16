import sys
from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QFileDialog
from PyQt5.QtGui import QIcon

import ui_mainwindow


class MainForm(object):
    def __init__(self):
        self.main_window = QMainWindow()
        self.main_ui = ui_mainwindow.Ui_MainWindow()
        self.main_ui.setupUi(self.main_window)
        self.main_window.show()

        self.main_file_dialog = QFileDialog()

        self.fun_main_ui_init()

    def fun_main_ui_init(self):
        self.main_ui.FileOpen.triggered.connect(self.fun_main_ui_file_open)
        self.main_ui.FileSave.triggered.connect(self.fun_main_ui_file_save)
        self.main_ui.statusbar.showMessage('test', 5000)
        self.main_ui.pushButton.setFixedSize(15, 15)
        self.main_ui.pushButton_2.setFixedSize(15, 15)
        self.main_ui.pushButton_3.setFixedSize(15, 15)
        self.main_ui.pushButton_3.clicked.connect(qApp.quit)

    def fun_main_ui_file_open(self):
        _path, _file = QFileDialog.getOpenFileName(
            self.main_file_dialog,
            'Save File', './', 'xls Files (*.xls)')
        print(_path, _file)

    def fun_main_ui_file_save(self):
        _path, _file = QFileDialog.getSaveFileName(
            self.main_file_dialog,
            'Save File', './', 'xls Files (*.xls)')
        print(_path, _file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    sys.exit(app.exec_())
