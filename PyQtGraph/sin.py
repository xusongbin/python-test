
import numpy as np
import pyqtgraph as pg

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

import ui_pg


class ModuleForm(object):
    def __init__(self):
        self.workWidget = QWidget()
        self.workUi = ui_pg.Ui_Form()
        self.workUi.setupUi(self.workWidget)

        self.win = pg.GraphicsWindow()
        self.win.resize(600, 400)
        self.win.setBackground('w')
        self.workUi.verticalLayout.addWidget(self.win)
        self.plot = self.win.addPlot()
        self.plot.showGrid(x=True, y=True)
        # self.plot.setLabel(axis='left', text='Amplitude / V')
        # self.plot.setLabel(axis='bottom', text='t / s')
        self.plot.setTitle('y1=sin(x) y2=cos(x)')
        # self.plot.addLegend()

        self.curve1 = self.plot.plot(pen='r', name='y1')
        self.curve2 = self.plot.plot(pen='g', name='y2')

        self.Fs = 1024.0    # 采样频率
        self.N = 1024       # 采样点数
        self.f0 = 3.0       # 信号频率
        self.pha = 0        # 初始相位
        self.t = np.arange(self.N) / self.Fs    # 时间向量

        self.timer = QTimer()
        self.timer.timeout.connect(self.set_data)
        self.timer.start(100)

    def set_data(self):
        self.pha += 10
        _tmp = 2 * np.pi * self.f0 * self.t + self.pha * np.pi / 180.0
        self.curve1.setData(self.t, np.sin(_tmp))
        self.curve2.setData(self.t, np.cos(_tmp))

    def show(self):
        self.workWidget.show()


def main():
    app = QApplication(sys.argv)
    mf = ModuleForm()
    mf.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
