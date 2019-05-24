
# 滑块实例

import sys
from PyQt5.QtWidgets import QWidget, QApplication

from QSlider_ex_ui import *


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.form_ui = Ui_Form()
        self.form_ui.setupUi(self)
        self.form_ui.retranslateUi(self)
        self.show()

        self.form_ui.label.setText('')
        self.form_ui.label_2.setText('')
        self.form_ui.label_3.setText('')

        self.form_ui.dial.valueChanged[int].connect(self.changevalue)
        self.form_ui.verticalSlider.valueChanged[int].connect(self.changevalue)
        self.form_ui.horizontalSlider.valueChanged[int].connect(self.changevalue)

    def changevalue(self, value):
        if self.sender() == self.form_ui.dial:
            self.form_ui.label_3.setText('dial：{:d}'.format(value))
        if self.sender() == self.form_ui.verticalSlider:
            self.form_ui.label_2.setText('verticalSlider：{:d}'.format(value))
        if self.sender() == self.form_ui.horizontalSlider:
            self.form_ui.label.setText('horizontalSlider：{:d}'.format(value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
