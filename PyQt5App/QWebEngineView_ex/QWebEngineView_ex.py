
# 使用内嵌网页引擎打开网址

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Form(QWebEngineView):
    def __init__(self):
        super(Form, self).__init__()

        self.load(QUrl("http://stockpage.10jqka.com.cn/300059"))
        self.show()
        print(self.page().profile().cookieStore().loadAllCookies())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    sys.exit(app.exec_())
