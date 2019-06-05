
# 拼图游戏

import os
import sys
import codecs
import pickle
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AppJigsaw_ui import *


class PuzzleShow(QWidget):
    puzzle_completed = pyqtSignal()
    drop_completed = pyqtSignal()

    def __init__(self, image_size):
        super().__init__()
        self.imageSize = image_size
        self.inPlace = 0
        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QRect()
        self.init_ui()

    def init_ui(self):
        self.setAcceptDrops(True)
        self.setMaximumSize(self.imageSize, self.imageSize)
        self.setMinimumSize(self.imageSize, self.imageSize)

    def dragEnterEvent(self, event):
        """
        鼠标移入准备拖动
        """
        if event.mimeData().hasFormat('image/x-puzzle'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """
        鼠标移开小窗口
        """
        update_rect = self.highlightedRect
        self.highlightedRect = QRect()
        self.update(update_rect)
        event.accept()

    def dragMoveEvent(self, event):
        """
        拖动
        """
        update_rect = self.highlightedRect.united(self.fun_target_square(event.pos()))
        if event.mimeData().hasFormat('image/x-puzzle') and \
                self.fun_find_piece(self.fun_target_square(event.pos())) == -1:
            self.highlightedRect = self.fun_target_square(event.pos())
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QRect()
            event.ignore()

        self.update(update_rect)

    def dropEvent(self, event):
        """
        拖动结束，图片落下
        """
        if event.mimeData().hasFormat('image/x-puzzle') and \
                self.fun_find_piece(self.fun_target_square(event.pos())) == -1:
            piece_data = event.mimeData().data('image/x-puzzle')
            data_stream = QDataStream(piece_data, QIODevice.ReadOnly)
            square = self.fun_target_square(event.pos())
            pixmap = QPixmap()
            location = QPoint()
            data_stream >> pixmap >> location

            self.pieceLocations.append(location)
            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.highlightedRect = QRect()
            self.update(square)

            event.setDropAction(Qt.MoveAction)
            event.accept()

            if location == QPoint(square.x() / self.fun_piece_size(), square.y() / self.fun_piece_size()):
                self.inPlace += 1
                if self.inPlace == 25:
                    self.puzzle_completed.emit()

        else:
            self.highlightedRect = QRect()
            event.ignore()

    def mousePressEvent(self, event):
        """
        鼠标按下事件
        """
        square = self.fun_target_square(event.pos())
        found = self.fun_find_piece(square)
        if found == -1:
            return

        location = self.pieceLocations[found]
        pixmap = self.piecePixmaps[found]
        del self.pieceLocations[found]
        del self.piecePixmaps[found]
        del self.pieceRects[found]

        if location == QPoint(square.x() / self.fun_piece_size(), square.y() / self.fun_piece_size()):
            self.inPlace -= 1

        self.update(square)

        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)

        data_stream << pixmap << location

        mime_data = QMimeData()
        mime_data.setData('image/x-puzzle', item_data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)

        if drag.exec(Qt.MoveAction) != Qt.MoveAction:
            self.pieceLocations.insert(found, location)
            self.piecePixmaps.insert(found, pixmap)
            self.pieceRects.insert(found, square)
            self.update(self.fun_target_square(event.pos()))

            if location == QPoint(square.x() / self.fun_piece_size(), square.y() / self.fun_piece_size()):
                self.inPlace += 1

    def paintEvent(self, event):
        """
        绘画事件
        """
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), Qt.white)
        if self.highlightedRect.isValid():
            painter.setBrush(QColor("#E6E6FA"))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for i in range(len(self.pieceRects)):
            painter.drawPixmap(self.pieceRects[i], self.piecePixmaps[i])
        painter.end()

    def fun_target_square(self, position):
        """
        拼图放下的矩形位置
        """
        x = position.x() // self.fun_piece_size() * self.fun_piece_size()
        y = position.y() // self.fun_piece_size() * self.fun_piece_size()
        return QRect(x, y, self.fun_piece_size(), self.fun_piece_size())

    def fun_find_piece(self, piece_rect):
        """
        找到拼图
        """
        try:
            return self.pieceRects.index(piece_rect)
        except ValueError:
            return -1

    def fun_piece_size(self):
        """
        单个拼图的大小
        """
        return int(self.imageSize // 5)

    def clear(self):
        """
        相关数据清空
        """
        self.piecePixmaps.clear()
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QRect()
        self.inPlace = 0
        self.update()


class PuzzlePiece(QListWidget):
    def __init__(self, piece_size):
        super().__init__()
        self.pieceSize = piece_size
        self.init_ui()

    def init_ui(self):
        self.setDragEnabled(True)
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(self.pieceSize, self.pieceSize))
        self.setSpacing(10)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """
        鼠标移入准备拖动
        """
        if event.mimeData().hasFormat('image/x-puzzle'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """
        拖动
        """
        if event.mimeData().hasFormat('image/x-puzzle'):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        拖动结束，图片落下
        """
        if event.mimeData().hasFormat('image/x-puzzle'):
            piece = event.mimeData().data('image/x-puzzle')
            data_stream = QDataStream(piece, QIODevice.ReadOnly)
            pixmap = QPixmap()
            location = QPoint()
            data_stream >> pixmap >> location
            self.fun_add_piece(pixmap, location)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, action):
        """
        开始拖
        """
        item = self.currentItem()
        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)
        piece_pix = item.data(Qt.UserRole)
        piece_location = item.data(Qt.UserRole + 1)
        data_stream << piece_pix << piece_location
        mime_data = QMimeData()
        mime_data.setData('image/x-puzzle', item_data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(piece_pix.width() / 2, piece_pix.height() / 2))
        drag.setPixmap(piece_pix)

        if drag.exec(Qt.MoveAction) == Qt.MoveAction:
            move_item = self.takeItem(self.row(item))
            del move_item

    def fun_add_piece(self, pix, loc):
        """
        增加一个拼图
        """
        puzzle_item = QListWidgetItem(self)
        puzzle_item.setIcon(QIcon(pix))
        puzzle_item.setData(Qt.UserRole, QVariant(pix))
        puzzle_item.setData(Qt.UserRole + 1, loc)
        puzzle_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)


class Jigsaw(QMainWindow):
    """
    拼图主程序
    """
    save_data = []
    file_path = "m.dat"

    def __init__(self, parent=None):
        """
        界面初始化
        载入历史时间
        记录时间初始化
        载入游戏
        """
        super(Jigsaw, self).__init__(parent)
        self.wui = Ui_MainWindow()
        self.wui.setupUi(self)

        ly = QHBoxLayout(self.wui.frame)
        self.puzzle_show = PuzzleShow(400)
        self.puzzle_piece = PuzzlePiece(self.puzzle_show.fun_piece_size())
        ly.addWidget(self.puzzle_piece)
        ly.addWidget(self.puzzle_show)
        self.setCentralWidget(self.wui.frame)

        self.work_message = QMessageBox(self)
        self.work_filedialog = QFileDialog(self)

        self.init_ui()

        self.puzzle_image = QPixmap("./img/Peppa.png")
        self.save_data = self.fun_load_time()

        self.timer = QTimer()
        self.timer.timeout.connect(self.second)
        self.time = 0

        self.setup_puzzle()

    def init_ui(self):
        """
        一些简单布局
        """
        self.wui.dockWidgetPicture.resize(400, 400)
        self.wui.label.setText('当前游戏用时：0秒，最佳时间：0秒')
        self.wui.label.setStyleSheet('color: rgb(255, 0, 0);font: 14pt "微软雅黑";')
        self.puzzle_show.puzzle_completed.connect(self.fun_set_completed)

        self.wui.actionaction_o.triggered.connect(self.fun_action_open)
        self.wui.actionaction_e.triggered.connect(self.fun_action_exit)
        self.wui.actionaction_r.triggered.connect(self.fun_action_restart)
        self.wui.actionaction_j.triggered.connect(self.fun_action_about)

    def fun_set_completed(self):
        """
        完成后弹出游戏结果对话框
        """
        self.timer.stop()
        self.save_data.append(self.time)
        self.fun_save_time()
        info = '恭喜通关成功！用时：{}秒，继续努力吧！\n按下OK继续！'.format(self.time)
        self.work_message.information(self, '通关成功', info, QMessageBox.Ok)

    def setup_puzzle(self):
        """
        游戏初始化
        """
        size = min(self.puzzle_image.width(), self.puzzle_image.height())

        self.puzzle_image = self.puzzle_image.copy(
            (self.puzzle_image.width() - size) / 2,
            (self.puzzle_image.height() - size) / 2,
            size,
            size
        ).scaled(
            self.puzzle_image.width(),
            self.puzzle_image.height(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )

        if self.puzzle_piece.count() > 1:
            self.puzzle_piece.clear()

        for y in range(5):
            for x in range(5):
                piece_size = self.puzzle_show.fun_piece_size()
                piece = self.puzzle_image.copy(x * piece_size, y * piece_size, piece_size, piece_size)
                self.puzzle_piece.fun_add_piece(piece, QPoint(x, y))

        for i in range(self.puzzle_piece.count()):
            if random.random() * 10 > 3:
                item = self.puzzle_piece.takeItem(i)
                self.puzzle_piece.insertItem(0, item)

        self.puzzle_show.clear()

        self.set_dock(self.puzzle_image)
        self.time = 0
        self.timing()

    def fun_load_time(self):
        """
        载入游戏时间数据
        """
        if not(os.path.exists(self.file_path) and os.path.isfile(self.file_path)):
            data = [100000]
            with codecs.open(self.file_path, 'wb') as f:
                pickle.dump(data, f)
        with codecs.open(self.file_path, 'rb') as f:
            data = pickle.load(f)
        return data

    def fun_save_time(self):
        """
        保存游戏时间
        """
        with codecs.open(self.file_path, 'wb') as f:
            pickle.dump(self.save_data, f)

    def timing(self):
        """
        开始计时
        """
        self.timer.start(1000)

    def second(self):
        """
        显示游戏时间
        """
        self.time += 1
        info = "当前游戏用时：{}秒，最佳时间：{}秒".format(self.time, min(self.save_data))
        self.wui.label.setText(info)

    def set_dock(self, pix):
        """
        显示还原后的图片
        """
        label2 = QLabel()
        label2.setScaledContents(True)
        label2.setPixmap(pix)
        self.wui.dockWidgetPicture.setWidget(label2)
        self.wui.dockWidgetPicture.setFloating(True)

    def fun_action_open(self):
        """
        选择图片并开始游戏
        """
        file = self.work_filedialog.getOpenFileName(self, "打开文件", "./img", ("Images (*.png *.jpg)"))
        path = file[0]
        if path:
            self.puzzle_image = QPixmap(path)
            self.wui.dockWidgetPicture.close()
            self.setup_puzzle()
            self.wui.dockWidgetPicture.show()
        else:
            self.work_message.warning(self, "打开图片", "图片加载失败！", QMessageBox.Cancel)
            return

    def fun_action_exit(self):
        """
        退出游戏
        """
        self.close()

    def fun_action_restart(self):
        """
        重新开始游戏
        """
        self.setup_puzzle()

    def fun_action_picture(self):
        """
        重新显示完成的图片
        """
        self.wui.dockWidgetPicture.close()
        self.wui.dockWidgetPicture.show()

    def fun_action_about(self):
        """
        关于
        """
        self.work_message.information(self, "关于", "学点编程吧出品，必属精品！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Jigsaw()
    exe.show()
    sys.exit(app.exec_())
