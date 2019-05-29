
# 表格装置实例，继承自QTableView，不能使用数据模型，可以设置复选框，不能与QSqlTableModel绑定

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QTableWidget_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.tableWidget.setRowCount(4)
        self.wui.tableWidget.setColumnCount(3)
        self.wui.tableWidget.setHorizontalHeaderLabels(['name', 'sex', 'weight'])

        people1 = ['ss', 'man', '80']
        for i, d in enumerate(people1):
            item = QTableWidgetItem(d)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.wui.tableWidget.setColumnWidth(i, 60)
            self.wui.tableWidget.setItem(0, i, item)

        # 将表格变为禁止编辑
        # self.wui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格为整行选择
        # self.wui.tableWidget.setSelectionBehavior( QAbstractItemView.SelectRows)

        # 将行和列的大小设为与内容相匹配
        # self.wui.tableWidget.resizeColumnsToContents()
        # self.wui.tableWidget.resizeRowsToContents()

        # 表格表头的显示与隐藏
        # self.wui.tableWidget.verticalHeader().setVisible(False)
        # self.wui.tableWidget.horizontalHeader().setVisible(False)

        # 不显示表格单元格的分割线
        # self.wui.tableWidget.setShowGrid(False)

        # 不显示垂直表头
        self.wui.tableWidget.verticalHeader().setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
