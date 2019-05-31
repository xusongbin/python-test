
# 通过鼠标事件获取选框位置绘制图形并截图

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from time import time

from QPainter_ex_ui import *


class Form(QWidget):
    def __init__(self):
        super().__init__()

        self.from_ui = Ui_Form()
        self.from_ui.setupUi(self)
        self.from_ui.retranslateUi(self)
        self.show()

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False

        self.screen = QApplication.primaryScreen()

    def mousePressEvent(self, QMouseEvent):
        self.flag = True
        self.x0 = QMouseEvent.x()
        self.y0 = QMouseEvent.y()

    def mouseReleaseEvent(self, QMouseEvent):
        self.flag = False
        if self.x1 > self.x0:
            _x = self.x0
            _w = self.x1 - self.x0
        else:
            _x = self.x1
            _w = self.x0 - self.x1
        if self.y1 > self.y0:
            _y = self.y0
            _h = self.y1 - self.y0
        else:
            _y = self.y1
            _h = self.y0 - self.y1
        pix = self.screen.grabWindow(
            # QApplication.desktop().winId(), _x, _y, _w, _h
            self.winId(), _x, _y, _w, _h
        )
        # pix.save("123.jpg")
        print('{:.3f}: save'.format(time()))

    def mouseMoveEvent(self, QMouseEvent):
        if self.flag:
            self.x1 = QMouseEvent.x()
            self.y1 = QMouseEvent.y()
            self.update()

    def paintEvent(self, QPaintEvent):
        if self.x1 > self.x0:
            _x = self.x0
            _w = self.x1 - self.x0
        else:
            _x = self.x1
            _w = self.x0 - self.x1
        if self.y1 > self.y0:
            _y = self.y0
            _h = self.y1 - self.y0
        else:
            _y = self.y1
            _h = self.y0 - self.y1
        rect = QRect(_x, _y, _w, _h)
        # print(_x, _y, _w, _h)
        p = QPainter(self)
        p.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        p.drawRect(rect)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())

'''
class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.x1 > self.x0:
            _x = self.x0
            _w = self.x1 - self.x0
        else:
            _x = self.x1
            _w = self.x0 - self.x1
        if self.y1 > self.y0:
            _y = self.y0
            _h = self.y1 - self.y0
        else:
            _y = self.y1
            _h = self.y0 - self.y1
        rect = QRect(_x, _y, _w, _h)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)

        pqscreen = QApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), _x, _y, _w, _h)
        pixmap2.save('123.jpg')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(675, 300)
        self.setWindowTitle('关注微信公众号：学点编程吧--opencv、PyQt5的小小融合')

        self.lb = myLabel(self)
        self.lb.setGeometry(QRect(140, 30, 511, 241))

        self.lb.setCursor(Qt.CrossCursor)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Example()
    sys.exit(app.exec_())
'''