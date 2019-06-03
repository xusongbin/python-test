
# 使用内嵌网页引擎打开网址

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.resize(900, 500)

        self.view = QWebEngineView(self)
        self.view.resize(self.size())
        url = 'http://stockpage.10jqka.com.cn/300059'
        url = 'http://www.baidu.com'
        url = QUrl(QFileInfo('web/index.html').absoluteFilePath())
        self.view.load(url)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    sys.exit(app.exec_())
