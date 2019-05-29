
# 堆栈装置实例1，类似TabWidget，没有标签页

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QStackedWidget_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.listWidget.currentRowChanged.connect(self.wui.stackedWidget.setCurrentIndex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
