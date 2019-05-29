
# 右键菜单功能演示

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QMenu_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wm = QMenu(self)
        self.wm.addAction(QAction('111', self.wm))
        self.wm.addAction(QAction('222', self.wm))
        self.wm.addAction(QAction('333', self.wm))

        self.wui.toolBox.customContextMenuRequested.connect(self.fun_menu)

    def fun_menu(self):
        self.wm.exec_(QCursor.pos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Example()
    run.show()
    sys.exit(app.exec_())
