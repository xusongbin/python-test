
import sys
from PyQt5.QtWidgets import QWidget, QApplication

from buddies_ex_ui import *


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        self.form_ui = Ui_Form()
        self.form_ui.setupUi(self)
        self.form_ui.retranslateUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
