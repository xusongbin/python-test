
import sys
from time import time
from PyQt5.QtWidgets import QDialog, QApplication

from pyPassword_ui import *


class Form(QDialog):
    def __init__(self):
        super(Form, self).__init__()

        self.form_ui = Ui_Dialog()
        self.form_ui.setupUi(self)
        self.form_ui.retranslateUi(self)
        self.show()

        self.text_len = 0
        self.text_str = ''
        self.text_old = ''
        self.form_ui.lineEdit.textChanged.connect(self.fun_edit_changed)

    def fun_edit_changed(self):
        _str = self.sender().text()
        _len = len(_str)
        if self.text_old == _len:
            return
        if self.text_len < _len:
            _show = _str[-1:]
            if self.text_len > 0:
                _show = '*' * self.text_len + _show
            self.text_old = len(_show)
            self.sender().setText(_show)
            self.text_len += 1
            self.text_str += _str[-1:]
        elif len(self.text_str) > 0:
            self.text_str = self.text_str[0:-1]
            self.text_len -= 1
            _show = self.text_str[-1:]
            if _len > 0:
                _show = '*' * (_len - 1) + _show
            self.text_old = len(_show)
            self.sender().setText(_show)
        self.form_ui.label.setText(self.text_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
