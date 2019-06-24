#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from drop_ui import *


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.work_ui = Ui_Form()
        self.work_ui.setupUi(self)
        self.setAcceptDrops(True)
        self.show()

        self.work_ui.lineEdit.setText('')
        self.work_ui.lineEdit.setAcceptDrops(False)

    # def dragEnterEvent(self, e):
    #     md = e.mimeData()
    #     assert isinstance(md, QMimeData)
    #     _text = md.text()
    #     if re.match(r'file:///.*\..+', _text):  # this is a file path
    #         _list = _text.split('\n')
    #         _result = []
    #         for _path in _list:
    #             _path = _path.strip()
    #             if _path == '':
    #                 continue
    #             _result.append(_path[8:])
    #         for i in _result:
    #             print('获取文件路径：%s' % i)
    #         self.work_ui.lineEdit.setText(_result[0])
    #     else:
    #         print('获取文本内容：%s' % _text)
    #     e.accept()

    def dragEnterEvent(self, e):
        assert isinstance(e, QDropEvent)
        e.acceptProposedAction()

    def dropEvent(self, e):
        assert isinstance(e, QDropEvent)
        if e.mimeData().hasUrls():
            print('urls:{}'.format(e.mimeData().urls()))
        else:
            print('text:{}'.format(e.mimeData().text()))
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())

