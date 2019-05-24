
# 树状装置实例2

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QTreeWidget_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.pushButtonAdd.clicked.connect(self.fun_btn_add)
        self.wui.pushButtonUpd.clicked.connect(self.fun_btn_upd)
        self.wui.pushButtonDel.clicked.connect(self.fun_btn_del)

        self.wui.treeWidget.setColumnCount(2)
        self.wui.treeWidget.setHeaderLabels(['key', 'value'])

        root = QTreeWidgetItem(self.wui.treeWidget)
        root.setText(0, 'root')
        root.setText(1, '0')

        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, '1')

        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, '2')

        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child3.setText(1, '3')

        child4 = QTreeWidgetItem(root)
        child4.setText(0, 'child4')
        child4.setText(1, '4')

        child5 = QTreeWidgetItem(root)
        child5.setText(0, 'child5')
        child5.setText(1, '5')

        self.wui.treeWidget.addTopLevelItem(root)
        self.wui.treeWidget.clicked.connect(self.fun_treewidget_clicked)

    def fun_btn_add(self):
        print('====add====')
        item = self.wui.treeWidget.currentItem()
        node = QTreeWidgetItem(item)
        node.setText(0, 'newNode')
        node.setText(1, 'x')

    def fun_btn_upd(self):
        print('====upd====')
        item = self.wui.treeWidget.currentItem()
        item.setText(0, 'update')
        item.setText(1, 'y')

    def fun_btn_del(self):
        print('====del====')
        root = self.wui.treeWidget.invisibleRootItem()
        assert isinstance(root, QTreeWidgetItem)
        for item in self.wui.treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def fun_treewidget_clicked(self):
        item = self.wui.treeWidget.currentItem()
        print('key=%s, value=%s' % (item.text(0), item.text(1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
