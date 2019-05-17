
import re
import sys
from ui_pack import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.work_ui = Ui_Form()
        self.work_ui.setupUi(self)
        self.work_ui.retranslateUi(self)
        self.setAcceptDrops(True)
        self.show()

        self.work_cnt = 0
        self.pos = None
        self.work_ui_init()

    def work_ui_init(self):
        self.work_ui.lineEdit.setText('')
        self.work_ui.lineEdit.setAcceptDrops(False)
        self.work_ui.labelKeyText.setText('')
        self.work_ui.labelKeyValue.setText('')
        self.work_ui.labelPosValue.setText('')
        self.work_ui.pushButton.clicked.connect(self.fun_btn_add)
        self.setMouseTracking(True)

    def fun_btn_add(self):
        self.work_cnt += 1
        self.work_ui.lineEdit.setText('%d' % self.work_cnt)

    def keyPressEvent(self, e):
        self.work_ui.labelKeyText.setText(e.text())
        self.work_ui.labelKeyValue.setText('%d' % e.key())

    def dragEnterEvent(self, e):
        _text = e.mimeData().text()
        if re.match(r'file:///.*\..+', _text):  # this is a file path
            _list = _text.split('\n')
            _result = []
            for _path in _list:
                _path = _path.strip()
                if _path == '':
                    continue
                _result.append(_path[8:])
            for i in _result:
                print('获取文件路径：%s' % i)
            self.work_ui.lineEdit.setText(_result[0])
        else:
            print('获取文本内容：%s' % _text)
        e.accept()

    def mouseMoveEvent(self, e):
        self.work_ui.labelPosValue.setText('{:d},{:d}'.format(e.x(), e.y()))
        self.pos = (e.x(), e.y())

    def paintEvent(self, e):
        if self.pos:
            q = QPainter(self)
            # q.drawLine(0, 0, self.pos[0], self.pos[1])
            q.drawEllipse(self.pos[0]-5, self.pos[1]-5, 10, 10)
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
