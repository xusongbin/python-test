
# 表格视图实例，可以设置数据模型，不能实现复选框，能够与QSqlTableModel绑定

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QTableView_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        model = QStandardItemModel(4, 4)
        model.setHorizontalHeaderLabels(['标题1', '标题2', '标题3', '标题4'])

        for row in range(4):
            for column in range(4):
                item = QStandardItem(str(row * 4 + column))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                model.setItem(row, column, item)
        self.wui.tableView.setModel(model)
        # self.wui.tableView.horizontalHeader().setStretchLastSection(True)
        self.wui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
