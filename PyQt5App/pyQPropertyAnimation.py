
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, QPoint

from pyQPropertyAnimation_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)
        self.show()

        self.wui.pushButton.clicked.connect(self.do_action)

        self.action = QPropertyAnimation(self.wui.pushButton, b'geometry')
        # self.action.setTargetObject(self.wui.pushButton)
        # self.action.setPropertyName(b'geometry')
        self.action.setDuration(1000)
        self.action.setStartValue(QRect(50, 50, 50, 25))
        self.action.setEndValue(QRect(50, 200, 50, 25))

    def do_action(self):
        self.action.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Example()
    sys.exit(app.exec_())

'''
import sys
from PyQt5.Qt import *
from PyQt5.QtCore import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('动画')
        self.resize(500, 500)
        self.move(400, 200)
        self.btn = QPushButton(self)
        self.init_ui()

    def init_ui(self):
        self.btn.resize(100, 100)
        self.btn.move(0, 0)
        self.btn.setStyleSheet('QPushButton{border: none; background: pink;}')

        # 1.定义一个动画
        animation = QPropertyAnimation(self)
        animation.setTargetObject(self.btn)
        animation.setPropertyName(b'pos')
        # 使用另外一种构造函数方式创建
        # animation = QPropertyAnimation(self.btn, b'pos', self)

        # 2.设置属性值
        animation.setStartValue(QPoint(0, 0))
        animation.setEndValue(QPoint(400, 400))

        # 3.设置时长
        animation.setDuration(3000)

        # 4.启动动画
        animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
'''