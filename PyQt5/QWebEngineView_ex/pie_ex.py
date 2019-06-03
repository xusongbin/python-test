
# 使用内嵌网页引擎打开网址

import sys
from random import randint

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *

from pie_ex_ui import *


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.view = QWebEngineView(self.wui.widget)
        self.view.setGeometry(0, 0, self.wui.widget.size().width(), self.wui.widget.size().height())
        url = QUrl(QFileInfo('pie/pie-simple.html').absoluteFilePath())
        self.view.load(url)

        self.time = QTimer()
        self.time.timeout.connect(self.autoshow)

        self.wui.checkBox.stateChanged.connect(self.checkbox)
        self.wui.spinBox_1.valueChanged.connect(self.showpie)
        self.wui.spinBox_2.valueChanged.connect(self.showpie)
        self.wui.spinBox_3.valueChanged.connect(self.showpie)
        self.wui.spinBox_4.valueChanged.connect(self.showpie)
        self.wui.spinBox_5.valueChanged.connect(self.showpie)
        self.wui.spinBox_6.valueChanged.connect(self.showpie)

    def checkbox(self, sta):
        if sta:
            self.time.start(1000)
        else:
            self.time.stop()

    def autoshow(self):
        self.wui.spinBox_1.setValue(randint(100, 10000))
        self.wui.spinBox_2.setValue(randint(100, 10000))
        self.wui.spinBox_3.setValue(randint(100, 1000))
        self.wui.spinBox_4.setValue(randint(100, 2000))
        self.wui.spinBox_5.setValue(randint(100, 3000))
        self.wui.spinBox_6.setValue(randint(100, 10000))

    def showpie(self):
        d1 = self.wui.spinBox_1.value()
        d2 = self.wui.spinBox_2.value()
        d3 = self.wui.spinBox_3.value()
        d4 = self.wui.spinBox_4.value()
        d5 = self.wui.spinBox_5.value()
        d6 = self.wui.spinBox_6.value()
        jscode = 'showPiChart({},{},{},{},{},{});'.format(d1, d2, d3, d4, d5, d6)
        print(jscode)
        self.view.page().runJavaScript(jscode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())
