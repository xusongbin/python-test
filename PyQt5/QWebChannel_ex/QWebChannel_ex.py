
# PyQt5 QtWebChannel 实现 Python脚本与网页Js脚本的数据传递

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import *

from QWebChannel_ex_ui import *


class Myshared(QWidget):
    finish = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def app_to_web(self):
        return "666"

    def web_to_app(self, data):
        self.finish.emit(data.split())

    value = pyqtProperty(str, fget=app_to_web, fset=web_to_app)


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)

        self.wmess = QMessageBox(self)
        self.channel = QWebChannel()
        self.shared = Myshared()

        self.view = QWebEngineView(self.wui.widget)
        self.view.setGeometry(0, 0, self.wui.widget.size().width(), self.wui.widget.size().height())
        url = QUrl(QFileInfo('web/webchannel.html').absoluteFilePath())
        self.view.load(url)

        self.channel.registerObject('connection', self.shared)
        self.view.page().setWebChannel(self.channel)
        self.shared.finish.connect(self.get_list)

        self.wui.pushButtonCommit.clicked.connect(self.btn_commit)
        self.wui.pushButtonCancel.clicked.connect(self.btn_cancel)

    def btn_commit(self):
        if not self.wui.lineEditUser.text():
            self.wmess.warning(self, '警告', '账户没有输入')
            self.wui.lineEditUser.setFocus()
        elif not self.wui.lineEditPwd.text():
            self.wmess.warning(self, '警告', '密码没有输入')
            self.wui.lineEditPwd.setFocus()
        else:
            user = self.wui.lineEditUser.text()
            pwd = self.wui.lineEditPwd.text()
            jscode = 'PyQt52WebValue(\'{}\', \'{}\');'.format(user, pwd)
            self.view.page().runJavaScript(jscode)
            _str = '发送数据=> 账户:{} 密码:{}'.format(user, pwd)
            self.wui.labelInfo.setText(_str)

    def btn_cancel(self):
        self.wui.lineEditUser.setText('')
        self.wui.lineEditPwd.setText('')
        self.wui.labelInfo.setText('')

    def get_list(self, info):
        self.wui.lineEditUser.setText(info[0])
        self.wui.lineEditPwd.setText(info[1])
        _str = '接收数据=> 账户:{} 密码:{}'.format(info[0], info[1])
        self.wui.labelInfo.setText(_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())
