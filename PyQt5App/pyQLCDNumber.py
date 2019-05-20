
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QDateTime, QDate, QTime
import sys

from pyQLCDNumber_ui import *


class Form(QWidget):
    def __init__(self):
        super().__init__()

        self.from_ui = Ui_Form()
        self.from_ui.setupUi(self)
        self.from_ui.retranslateUi(self)
        self.show()

        self.time = QTimer()
        self.time.timeout.connect(self.fun_refresh)
        self.time.start(10)

    def fun_refresh(self):
        start = QDateTime.currentMSecsSinceEpoch()
        # end = QDateTime(QDate(2020, 1, 20), QTime(0, 0, 0)).toMSecsSinceEpoch()
        end = self.from_ui.dateEdit.dateTime().toMSecsSinceEpoch()
        interval = end - start
        if interval > 0:
            days = int(interval / (24 * 60 * 60 * 1000))
            hour = int((interval - days * 24 * 60 * 60 * 1000) / (60 * 60 * 1000))
            min = int((interval - days * 24 * 60 * 60 * 1000 - hour * 60 * 60 * 1000) / (60 * 1000))
            sec = int((interval - days * 24 * 60 * 60 * 1000 - hour * 60 * 60 * 1000 - min * 60 * 1000) / 1000)
            intervals = '{:d}-{:0>2}:{:0>2}:{:0>2}'.format(days, hour, min, sec)
            self.from_ui.lcdNumber.display(intervals)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = Form()
    sys.exit(app.exec_())
