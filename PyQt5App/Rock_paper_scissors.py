
import sys
from random import randint
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from Rock_paper_scissors_ui import *


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.form_ui = Ui_Form()
        self.form_ui.setupUi(self)
        self.form_ui.retranslateUi(self)
        self.show()

        self.key_dict = {1: '石头', 2: '剪刀', 3: '布'}
        self.fun_ui_init()

    def fun_ui_init(self):
        self.form_ui.pushButton1.clicked.connect(self.fun_btn_click)
        self.form_ui.pushButton2.clicked.connect(self.fun_btn_click)
        self.form_ui.pushButton3.clicked.connect(self.fun_btn_click)

    def fun_btn_click(self):
        _text = self.sender().text()
        if _text == '石头':
            _player = 1
        elif _text == '剪刀':
            _player = 2
        else:
            _player = 3
        _cp = randint(1, 3)
        if _cp == _player:
            QMessageBox.about(self, '结果', '电脑：{} 平手'.format(self.key_dict[_cp]))
        elif _player == 1 and _cp == 2:
            QMessageBox.about(self, '结果', '电脑：{} 玩家赢了!'.format(self.key_dict[_cp]))
        elif _player == 2 and _cp == 3:
            QMessageBox.about(self, '结果', '电脑：{} 玩家赢了!'.format(self.key_dict[_cp]))
        elif _player == 3 and _cp == 1:
            QMessageBox.about(self, '结果', '电脑：{} 玩家赢了!'.format(self.key_dict[_cp]))
        elif _player == 2 and _cp == 1:
            QMessageBox.about(self, '结果', '电脑：{} 电脑赢了!'.format(self.key_dict[_cp]))
        elif _player == 3 and _cp == 2:
            QMessageBox.about(self, '结果', '电脑：{} 电脑赢了!'.format(self.key_dict[_cp]))
        elif _player == 1 and _cp == 3:
            QMessageBox.about(self, '结果', '电脑：{} 电脑赢了!'.format(self.key_dict[_cp]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
