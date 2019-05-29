
# 子窗口控件实例1，包含QToolBar和QAction用法

import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QMdiArea_ex_ui import *


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_MainWindow()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'a', 'j', 'joker', 'k', 'q']

        self.wui.actionaction1.triggered.connect(self.send_one)
        self.wui.actionaction2.triggered.connect(self.send_five)
        self.wui.actionaction3.triggered.connect(self.set_clear)
        self.wui.actionaction4.triggered.connect(self.set_fold)

    def send_one(self):
        name = self.random_cards(1)
        sub = QMdiSubWindow()
        self.wui.mdiArea.addSubWindow(sub)
        sub.setWindowTitle(name)
        sub.setWindowFlags(Qt.WindowMinimizeButtonHint)
        sub.resize(150, 200)
        sub.show()

    def send_five(self):
        names = self.random_cards(5)
        for name in names:
            sub = QMdiSubWindow()
            self.wui.mdiArea.addSubWindow(sub)
            sub.setWindowTitle(name)
            sub.setWindowFlags(Qt.WindowMinimizeButtonHint)
            sub.resize(150, 200)
            sub.show()

    def set_clear(self):
        self.wui.mdiArea.closeAllSubWindows()

    def set_fold(self):
        self.wui.mdiArea.cascadeSubWindows()

    def random_cards(self, num):
        if num == 1:
            return random.choice(self.cards)
        elif num == 5:
            return random.sample(self.cards, 5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
