
# 滚动条，扩大当前窗口的有效装载面积

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QScrollBar_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.horizontalScrollBar.sliderMoved.connect(self.scroll_val)
        self.wui.verticalScrollBar.sliderMoved.connect(self.scroll_val)
        self.wui.verticalScrollBar_2.sliderMoved.connect(self.scroll_val)

    def scroll_val(self):
        s1 = self.wui.horizontalScrollBar.value()
        s2 = self.wui.verticalScrollBar.value()
        s3 = self.wui.verticalScrollBar_2.value()
        print('value: {}, {}, {}'.format(s1, s2, s3))
        pal = QPalette()
        c = QColor(s1, s2, s3, 255)
        pal.setColor(QPalette.Foreground, c)
        self.wui.label.setPalette(pal)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
