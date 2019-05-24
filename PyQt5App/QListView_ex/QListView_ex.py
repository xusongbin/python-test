
# 清单视图实例

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

        items = ['1', 'a', '66']
        listmodel = QStringListModel()
        listmodel.setStringList(items)
        self.wui.listView.setModel(listmodel)
        self.wui.listView.doubleClicked.connect(self.fun_listview_dclick)

    def fun_listview_dclick(self, idx):
        print(idx.data())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
