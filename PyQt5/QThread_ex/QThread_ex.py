
# 线程实例

import sys
from time import sleep, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Example(QWidget):

    class myThread(QThread):
        finish = pyqtSignal(str)

        def __init__(self, parent=None):
            super().__init__(parent)

        def run(self):
            t = time()
            self.finish.emit('start.{}'.format(t))
            for i in range(5):
                sleep(0.1)
                self.finish.emit(str(i))
            t = time()
            self.finish.emit('done.{}'.format(t))

    def __init__(self):
        super().__init__()
        self.bt1 = QPushButton('开始', self)
        self.bt1.move(100, 20)

        self.t = self.myThread()
        self.t.finish.connect(self.fun_show_print)

        self.bt1.clicked.connect(self.fun_btn_click)

    def fun_btn_click(self):
        self.t.start()

    def fun_show_print(self, msg):
        print('message:', msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Example()
    run.show()
    sys.exit(app.exec_())
