
# 选项框实例，调用网页浏览器打开网址

import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget

from QToolBox_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)
        self.show()

        self.wui.toolButtonBaidu.clicked.connect(self.fun_btn_clicked)
        self.wui.toolButtonSougo.clicked.connect(self.fun_btn_clicked)
        self.wui.toolButtonTengxun.clicked.connect(self.fun_btn_clicked)

    def fun_btn_clicked(self):
        if self.sender() == self.wui.toolButtonBaidu:
            webbrowser.open('https://www.baidu.com')
        elif self.sender() == self.wui.toolButtonSougo:
            webbrowser.open('https://www.sogou.com/')
        elif self.sender() == self.wui.toolButtonTengxun:
            webbrowser.open('https://v.qq.com')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Example()
    sys.exit(app.exec_())
