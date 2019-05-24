
# 富文本插入图片实例

import sys
from io import BytesIO
from PIL import Image
from requests import get
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QTextEdit_ex_ui import *


def get_shape(dw, dh, w1, h1):
    k0 = dw / dh
    k1 = w1 / h1

    if k0 > k1:     # h
        h = h1
        if h1 > dh:
            h = dh
        w = int(h * k1)
    else:           # w
        w = w1
        if w1 > dw:
            w = dw
        h = int(w / k1)
    return w, h


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.wui.pushButton.clicked.connect(self.fun_btn_click)

    def fun_btn_click(self):
        _url = self.wui.lineEdit.text()
        if not _url:
            return
        self.wui.lineEdit.setText('')
        try:
            filepath = '123.png'
            response = get(_url)
            image = Image.open(BytesIO(response.content))
            assert isinstance(image, Image.Image)
            image.save(filepath)
            del image
            image = QImage(filepath)
            width, height = get_shape(400, 260, image.width(), image.height())
            self.wui.textEdit.setHtml('<img src="{}"  height="{}" width="{}" />'.format(filepath, height, width))
        except:
            pass


def run():
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
    # print(get_shape(400, 260, 450, 270))
