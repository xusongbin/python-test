
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class Form(QWebEngineView):
    def __init__(self):
        super(Form, self).__init__()

        self.load(QUrl("http://www.baidu.com"))
        self.show()
        print(self.page().profile().cookieStore())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    sys.exit(app.exec_())
