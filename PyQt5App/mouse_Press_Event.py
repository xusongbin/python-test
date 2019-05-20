
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject

from mouse_Press_Event_ui import *


class Signal(QObject):
    showmouse = pyqtSignal()


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.form_ui = Ui_Form()
        self.form_ui.setupUi(self)
        self.form_ui.retranslateUi(self)
        self.show()

        self.s = Signal()
        self.s.showmouse.connect(self.fun_btn_click)

    def fun_btn_click(self):
        QMessageBox.about(self, '鼠标', '点击了鼠标左键！')

    def mousePressEvent(self, e):
        self.s.showmouse.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
