
# 模拟QQ好友列表

import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

name_str = (
    '恨桃、依秋、依波、香巧、紫萱、涵易、忆之、幻巧、水风、安寒、白亦、惜玉、碧春、怜雪、听南、念蕾、紫夏、凌旋、芷梦、凌寒、'
    '梦竹、千凡、采波、元冬、思菱、平卉、笑柳、雪卉、南蓉、谷梦、巧兰、绿蝶、飞荷、平安、芷荷、怀瑶、慕易、若芹、紫安、曼冬、'
    '寻巧、寄波、尔槐、以旋、初夏、依丝、怜南、傲菡、谷蕊、笑槐、飞兰、笑卉、迎荷、元冬、痴安、妙绿、觅雪、寒安、沛凝、白容、'
    '乐蓉、映安、依云、映冬、凡雁、梦秋、梦凡、秋巧、若云、元容、怀蕾、灵寒、天薇、翠安、乐琴、宛南、怀蕊、白风、访波、亦凝、'
    '易绿、夜南、曼凡、亦巧、青易、冰真、白萱、友安、海之、小蕊、又琴、天风、若松、盼菡、秋荷、香彤、语梦、惜蕊、迎彤、沛白、'
    '雁山、易蓉、雪晴、诗珊、春冬、又绿、冰绿、半梅、笑容、沛凝、映秋、盼烟、晓凡、涵雁、问凝、冬萱、晓山、雁蓉、梦蕊、山菡、'
    '南莲、飞双、凝丝、思萱、怀梦、雨梅、冷霜、向松、迎丝、迎梅、雅彤、香薇、以山、碧萱、寒云、向南、书雁、怀薇、思菱、忆文、'
    '翠巧、怀山、若山、向秋、凡白、绮烟、从蕾、天曼、又亦、从安、绮彤、之玉、凡梅、依琴、沛槐、又槐、元绿、安珊、夏之、易槐、'
    '宛亦、白翠、丹云、问寒、易文、傲易、青旋、思真、雨珍、幻丝、代梅、盼曼、妙之、半双、若翠、初兰、惜萍、初之、宛丝、寄南、'
    '小萍、静珊、千风、天蓉、雅青、寄文、涵菱、香波、青亦、元菱、翠彤、春海、惜珊、向薇、冬灵、惜芹、凌青、谷芹、雁桃、映雁、'
    '书兰、盼香、向山、寄风、访烟、绮晴、映之、醉波、幻莲、谷冬、傲柔、寄容、以珊、紫雪、芷容、书琴、寻桃、涵阳、怀寒、易云、'
    '代秋、惜梦、尔烟、谷槐、怀莲、夜山、芷卉、向彤、新巧、语海、灵珊、凝丹、小蕾、迎夏、慕卉、飞珍、冰夏、亦竹、飞莲、海白、'
    '元蝶、春蕾、怀绿、尔容、小玉、幼南、凡梦、碧菡、初晴、宛秋、傲旋、新之、凡儿、夏真、静枫、痴柏、恨蕊、乐双、念薇、靖雁、'
    '寄松、丹蝶、元瑶、冰蝶、念波、迎松、海瑶、乐萱、凌兰、曼岚、若枫、傲薇、凡灵、乐蕊、秋灵、谷槐、觅云、寻春、恨山、从寒、'
    '觅波、静曼、青寒、笑天、涵蕾、元柏、代萱、紫真、千青、雪珍、寄琴、绿蕊、醉柳、诗翠、念瑶、孤风、曼彤、怀曼、香巧、采蓝'
)
name_list = name_str.split('、')


def get_random_name():
    global name_list
    num = random.randint(0, len(name_list))
    name = name_list[num]
    name_list.remove(name)
    return name


class ListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.ListItemData = []
        self.Data_init()

    def data(self, index, role):
        if index.isValid() or (0 <= index.row() < len(self.ListItemData)):
            if role == Qt.DisplayRole:
                return QVariant(self.ListItemData[index.row()]['name'])
            elif role == Qt.DecorationRole:
                return QVariant(QIcon(self.ListItemData[index.row()]['iconPath']))
            elif role == Qt.SizeHintRole:
                return QVariant(QSize(70, 80))
            elif role == Qt.TextAlignmentRole:
                return QVariant(int(Qt.AlignHCenter | Qt.AlignVCenter))
            elif role == Qt.FontRole:
                font = QFont()
                font.setPixelSize(20)
                return QVariant(font)
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.ListItemData)

    def Data_init(self):
        randomnum = random.sample(range(26), 10)
        for i in randomnum:
            _dict = {}.clear()
            _dict['name'] = get_random_name()
            _dict['iconPath'] = 'image/%d.jpg' % i
            self.ListItemData.append(_dict)

    def addItem(self, itemData):
        if itemData:
            self.beginInsertRows(QModelIndex(), len(self.ListItemData), len(self.ListItemData) + 1)
            self.ListItemData.append(itemData)
            self.endInsertRows()

    def deleteItem(self, index):
        del self.ListItemData[index]

    def getItem(self, index):
        if -1 < index < len(self.ListItemData):
            return self.ListItemData[index]


class ListWidget(QListWidget):
    map_listwidget = []

    def __init__(self):
        super().__init__()
        self.Data_init()
        self.Ui_init()

    def Data_init(self):
        randomnum = random.sample(range(26), 10)
        for i in randomnum:
            item = QListWidgetItem()
            randname = get_random_name()
            randicon = 'image/%d.jpg' % i
            font = QFont()
            font.setPointSize(16)
            item.setFont(font)
            item.setText(randname)
            flag = random.randint(0, 5)
            if flag == 1:
                item.setForeground(QBrush(Qt.red))
            item.setToolTip('会员红名尊享')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setIcon(QIcon(randicon))
            self.addItem(item)

    def Ui_init(self):
        self.setIconSize(QSize(70, 70))
        self.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                           "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                           "QListWidget::Item:hover{background:skyblue; }"
                           "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
                           )
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemSelectionChanged.connect(self.getListitems)

    def getListitems(self):
        return self.selectedItems()

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            if self is self.find('我的好友'):
                pAddItem = QAction("新增好友", pmenu)
                pmenu.addAction(pAddItem)
                pAddItem.triggered.connect(self.addItemSlot)
            if len(self.map_listwidget) > 1:
                pSubMenu = QMenu("转移联系人至", pmenu)
                pmenu.addMenu(pSubMenu)
                try:
                    for item_dic in self.map_listwidget:
                        if item_dic['listwidget'] is not self:
                            pMoveAct = QAction(item_dic['groupname'], pmenu)
                            pSubMenu.addAction(pMoveAct)
                            pMoveAct.triggered.connect(self.move)
                except Exception as e:
                    print('map_listwidget: %s' % e)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        dellist = self.getListitems()
        for delitem in dellist:
            del_item = self.takeItem(self.row(delitem))
            del del_item

    def addItemSlot(self):
        '''
        dg = Dialog_additem()
        r = dg.exec()
        if r > 0:
            newitem = QListWidgetItem()
            newname = dg.lineEdit.text()
            newicon = dg.geticonpath()
            font = QFont()
            font.setPointSize(16)
            newitem.setFont(font)
            newitem.setText(newname)
            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newitem.setIcon(QIcon(newicon))
            self.addItem(newitem)
        '''
        groupname = QInputDialog.getText(self, "输入好友名称", "")
        if groupname[0] and groupname[1]:
            newitem = QListWidgetItem()
            newname = groupname[0]
            newicon = None
            font = QFont()
            font.setPointSize(16)
            newitem.setFont(font)
            newitem.setText(newname)
            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newitem.setIcon(QIcon(newicon))
            self.addItem(newitem)
        elif groupname[0] == '' and groupname[1]:
            QMessageBox.warning(self, "警告", "我说你没有填写好友名哦~！")


    def setListMap(self, listwidget):
        self.map_listwidget.append(listwidget)

    def move(self):
        tolistwidget = self.find(self.sender().text())
        movelist = self.getListitems()
        for moveitem in movelist:
            pItem = self.takeItem(self.row(moveitem))
            tolistwidget.addItem(pItem)

    def find(self, pmenuname):
        print(pmenuname)
        print(self.map_listwidget)
        try:
            for item_dic in self.map_listwidget:
                if item_dic['groupname'] == pmenuname:
                    return item_dic['listwidget']
        except Exception as e:
            print('find e:%s' % e)

'''
class ListView(QListView):
    map_listview = []

    def __init__(self):
        super().__init__()
        self.m_pModel = ListModel()
        self.setModel(self.m_pModel)

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            pSubMenu = QMenu("转移联系人至", pmenu)
            pmenu.addMenu(pSubMenu)
            for item_dic in self.map_listview:
                pMoveAct = QAction(item_dic['groupname'], pmenu)
                pSubMenu.addAction(pMoveAct)
                pMoveAct.triggered.connect(self.move)
            pmenu.popup(self.mapToGlobal(event.pos()))

    def deleteItemSlot(self):
        index = self.currentIndex().row()
        if index > -1:
            self.m_pModel.deleteItem(index)

    def setListMap(self, listview):
        self.map_listview.append(listview)

    def addItem(self, pitem):
        self.m_pModel.addItem(pitem)

    def move(self):
        tolistview = self.find(self.sender().text())
        if tolistview is self:
            prelistview = self.sender().text()
            QMessageBox.warning(self, "警告", "该联系人就在{}，还怎么移动啊！".format(prelistview))
        else:
            index = self.currentIndex().row()
            pItem = self.m_pModel.getItem(index)
            tolistview.addItem(pItem)
            self.m_pModel.deleteItem(index)

    def find(self, pmenuname):
        for item_dic in self.map_listview:
            if item_dic['groupname'] == pmenuname:
                return item_dic['listview']
'''


class QQ(QToolBox):
    def __init__(self):
        super().__init__()
        # pListView = ListView()
        pListView = ListWidget()
        pListView.setViewMode(QListView.ListMode)
        pListView.setStyleSheet("QListView{icon-size:70px}")
        dic_list = {'listview': pListView, 'groupname': "我的好友"}
        pListView.setListMap(dic_list)
        self.addItem(pListView, "我的好友")
        self.resize(270, 600)
        self.show()

    def contextMenuEvent(self, event):
        pmenu = QMenu(self)
        pAddGroupAct = QAction("添加分组", pmenu)
        pmenu.addAction(pAddGroupAct)
        pAddGroupAct.triggered.connect(self.addGroupSlot)
        pmenu.popup(self.mapToGlobal(event.pos()))

    def addGroupSlot(self):
        groupname = QInputDialog.getText(self, "输入分组名", "")
        if groupname[0] and groupname[1]:
            pListView1 = ListWidget()
            pListView1.setViewMode(QListView.ListMode)
            pListView1.setStyleSheet("QListView{icon-size:70px}")
            self.addItem(pListView1, groupname[0])
            dic_list = {'listview': pListView1, 'groupname': groupname[0]}
            pListView1.setListMap(dic_list)
        elif groupname[0] == '' and groupname[1]:
            QMessageBox.warning(self, "警告", "我说你没有填写分组名哦~！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = QQ()
    sys.exit(app.exec_())
