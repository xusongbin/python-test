#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import time
from langdetect import detect, detect_langs

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from langdetect_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.lineEditInput.returnPressed.connect(self.check_input)

    def check_input(self):
        tms = time()
        _text = self.wui.lineEditInput.text()
        print('输入内容：', _text)
        self.wui.lineEditResult.setText(detect(_text))
        print('检测耗时：%.3f' % (time() - tms))
        print(detect_langs(_text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
