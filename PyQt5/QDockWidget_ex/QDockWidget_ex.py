
# MainWindow窗口Dock停靠控件实例1

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QDockWidget_ex_ui import *


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_MainWindow()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
