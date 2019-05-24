
# 树状装置实例1

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

        self.wui.treeWidget.setColumnCount(2)
        self.wui.treeWidget.setHeaderLabels(['key', 'value'])

        # 设置根节点
        root = QTreeWidgetItem(self.wui.treeWidget)
        root.setText(0, 'root')
        root.setIcon(0, QIcon('image/root.jpg'))

        # 设置列宽
        self.wui.treeWidget.setColumnWidth(0, 150)

        # 设置节点的背景颜色
        # brush_red = QBrush(Qt.red)
        # root.setBackground(0, brush_red)
        # brush_green = QBrush(Qt.green)
        # root.setBackground(1, brush_green)

        # 设置子节点1
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'main1')
        child1.setText(1, 'value1')
        child1.setIcon(0, QIcon('image/1.jpg'))
        child1.setCheckState(0, Qt.Checked)  # 设置选项已被选中状态

        # 设置子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'main2')
        child2.setText(1, '')
        child2.setIcon(0, QIcon('image/2.jpg'))
        child2.setCheckState(0, Qt.Unchecked)

        # 设置子节点3,子节点2的子节点
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child1')
        child3.setText(1, 'value3')
        child3.setIcon(0, QIcon('image/3.jpg'))
        child3.setCheckState(0, Qt.Unchecked)

        # 为tree增加顶级项目
        self.wui.treeWidget.addTopLevelItem(root)
        # 结点全部展开
        self.wui.treeWidget.expandAll()

        self.wui.treeWidget.itemClicked.connect(self.fun_item_clicked)

    def fun_item_clicked(self, item, idx):
        print(idx)
        assert isinstance(item, QTreeWidgetItem)
        if item.checkState(0):
            sta = Qt.Checked
        else:
            sta = Qt.Unchecked
        for i in range(item.childCount()):
            item.child(i).setCheckState(i, sta)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
