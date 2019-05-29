
# 纯文本框行，选中行修改背景色

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from QPlainTextEdit_ex_ui import *


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)
        self.wui.retranslateUi(self)

        self.line_num = None

        self.wui.plainTextEdit.cursorPositionChanged.connect(self.fun_highlight_line)

    # def resizeEvent(self, e):
    #     cr = self.wui.plainTextEdit.contentsRect()
    #     rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
    #     self.number_bar.setGeometry(rec)

    def fun_highlight_line(self):
        num = self.wui.plainTextEdit.textCursor().blockNumber()
        if self.line_num != num:
            self.line_num = num
            hs = QTextEdit.ExtraSelection()
            hs.format.setBackground(QColor(Qt.green).lighter(160))
            hs.format.setProperty(QTextFormat.FullWidthSelection, True)
            hs.cursor = self.wui.plainTextEdit.textCursor()
            hs.cursor.clearSelection()
            self.wui.plainTextEdit.setExtraSelections([hs])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
