#!/usr/bin/env python

import sys
import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class AnalogClock(QWidget):
    hourHand = QPolygon([
        QPoint(2, 2),
        QPoint(-2, 2),
        QPoint(-2, -50),
        QPoint(2, -50)
    ])
    minuteHand = QPolygon([
        QPoint(1.5, 1.5),
        QPoint(-1.5, 1.5),
        QPoint(-1.5, -65),
        QPoint(1.5, -65)
    ])
    secondHand = QPolygon([
        QPoint(1.0, 1.0),
        QPoint(-1.0, 1.0),
        QPoint(-1.0, -80),
        QPoint(1.0, -80)
    ])

    hourColor = QColor(0, 170, 0)
    minuteColor = QColor(85, 0, 255)
    secondColor = QColor(50, 50, 50)

    def __init__(self, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(100)

        self.setWindowTitle("Analog Clock")
        self.resize(500, 500)

        self.lb = QLabel(self)
        self.lb.setGeometry(1, 1, 120, 15)

    def paintEvent(self, event):
        self.lb.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))

        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 250, side / 250)

        painter.restore()
        painter.setPen(self.hourColor)
        painter.save()
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30)

        painter.restore()
        painter.setPen(self.minuteColor)
        painter.save()
        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6)

        painter.restore()
        painter.setPen(self.secondColor)
        painter.save()
        for i in range(1, 13):
            _text = '%d' % i
            _len = len(_text)
            k = 1.6
            _offset = _len * k
            painter.rotate(30 - _offset)
            painter.drawText(0, -100, _text)
            painter.rotate(_offset)

        painter.restore()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.hourColor)
        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.drawConvexPolygon(self.hourHand)

        painter.restore()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.minuteColor)
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)

        painter.restore()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.secondColor)
        painter.save()
        painter.rotate(6.0 * time.second())
        painter.drawConvexPolygon(self.secondHand)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AnalogClock()
    clock.show()
    sys.exit(app.exec_())
