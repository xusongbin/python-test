
# 清单装置实例，继承自QListView，集成QListWidgetItem数据存储模型

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QListWidget_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.listWidget.addItem('AA')
        self.wui.listWidget.addItem('BB')
        self.wui.listWidget.addItem('CC')
        self.wui.listWidget.addItem('DD')
        self.wui.listWidget.addItem('EE')
        self.wui.listWidget.setWindowTitle('123')
        self.wui.listWidget.itemClicked.connect(self.fun_listwidget_clicked)

    def fun_listwidget_clicked(self, item):
        print(item.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
