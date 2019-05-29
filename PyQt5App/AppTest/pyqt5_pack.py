
import sys
import ui_pack
from PyQt5.QtWidgets import QApplication, QWidget


class Form(object):
    def __init__(self):
        self.work_widget = QWidget()
        self.work_ui = ui_pack.Ui_Form()
        self.work_ui.setupUi(self.work_widget)
        self.work_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
