
import sys
from ui_pack import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.work_ui = Ui_Form()
        self.work_ui.setupUi(self)
        self.work_ui.retranslateUi(self)
        self.show()

        self.work_cnt = 0
        self.work_ui_init()

    def work_ui_init(self):
        self.work_ui.lineEdit.setText('')
        self.work_ui.labelKeyText.setText('')
        self.work_ui.labelKeyValue.setText('')
        self.work_ui.pushButton.clicked.connect(self.fun_btn_add)

    def fun_btn_add(self):
        self.work_cnt += 1
        self.work_ui.lineEdit.setText('%d' % self.work_cnt)

    def keyPressEvent(self, e):
        self.work_ui.labelKeyText.setText(e.text())
        self.work_ui.labelKeyValue.setText('%d' % e.key())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
