
# 带图标的清单视图

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QListView_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.listView.setIconSize(QSize(40, 40))
        self.wui.listView.setGridSize(QSize(60, 45))

        item1 = QStandardItem(QIcon('ico/1.ico'), 'AAAAA')
        item2 = QStandardItem(QIcon('ico/1.ico'), 'BBBBB')
        mode1 = QStandardItemModel()
        mode1.appendRow(item1)
        mode1.appendRow(item2)
        self.wui.listView.setModel(mode1)

        self.wui.listView.doubleClicked.connect(self.fun_listview_dclick)

    def fun_listview_dclick(self, idx):
        print(idx.data())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
