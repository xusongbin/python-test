
import numpy as np
import pyqtgraph as pg

import re
import sys
import cmath
import queue
from time import time, sleep, strftime, localtime
import serial
from serial.tools import list_ports

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer

import ui_pg

module_port_id = 'VID:PID=0483:374B'


def write_log(_data):
    _data = strftime("%Y-%m-%d %H:%M:%S ", localtime()) + _data
    try:
        print(_data)
        with open('log.txt', 'a+') as f:
            f.write(_data + '\n')
    except Exception as e:
        print('write log exception %s' % e)


class Serial(object):
    def __init__(self, hid, baud, timeout, com=''):
        self.baud = baud
        self.byte = 8
        self.parity = serial.PARITY_NONE
        self.stopbits = 1

        self.hid = hid
        self.receive = ''
        self.buffer = ''
        self.timeout = timeout
        self.port = None
        self.open = False
        self.com = com
        self.name = ''
        if not com == '':
            self.name = com
        self.rx_queue = queue.Queue()

    def get_valid(self):
        return self.open

    @staticmethod
    def get_port_name():
        _list = []
        for comport in list_ports.comports():
            name = str(comport)
            name = name.split(' ')[0]
            _list.append(name)
        return _list

    def get_port_by_hid(self, hid=''):
        if hid == '':
            hid = self.hid
        for comport in list_ports.comports():
            if hid in comport.hwid:
                name = str(comport)
                name = name.split(' ')[0]
                return name
        return ''

    def get_receive_str(self):
        return self.receive

    def get_receive_line(self):
        return self.receive.split('\r')[0].strip()

    def set_open(self):
        try:
            self.port = serial.Serial(
                port=self.name,
                baudrate=self.baud,
                bytesize=self.byte,
                stopbits=self.stopbits,
                parity=self.parity,
                timeout=0)
            write_log('open port successful %s' % self.name)
            self.open = True
            return True
        except Exception as e:
            print('open port failure %s %s' % (self.name, e))
            return False

    def set_close(self):
        try:
            self.port.close()
        except Exception as e:
            print('close port failure %s' % e)
            return False

    def set_reopen(self):
        self.open = False
        if self.com == '':
            self.name = self.get_port_by_hid()
        else:
            self.name = self.com
        if self.name == '':
            return False
        self.set_close()
        return self.set_open()

    def set_send(self, tx, rx, wakeup=False):
        self.receive = ''
        self.buffer = ''
        if tx != '':
            try:
                if wakeup:
                    self.port.write(b'\xff\xff\xff\xff')
                self.port.write(tx.encode('utf-8'))
                write_log('TX %s:%s' % (self.name, tx))
            except Exception as e:
                # print('send serial exception %s' % e)
                self.set_reopen()
                if self.open is True:
                    self.port.write(tx.encode('utf-8'))
                else:
                    return False
        # print(int(time() * 1000))
        # if rx == '':
        #     return True

        _start = int(round(time() * 1000))
        _now = int(round(time() * 1000))
        while _now - _start < self.timeout:
            line = ''
            try:
                if self.port.inWaiting() > 0:
                    line = self.port.readline()
            except Exception as e:
                print('receive serial exception %s' % e)
                self.set_reopen()
                if self.open is False:
                    return False
            if line != '':
                self.buffer += line.decode("utf-8", "ignore")
                _start = int(round(time() * 1000))
            _now = int(round(time() * 1000))
            sleep(0.01)
        if self.buffer != '':
            write_log('RX %s:%s' % (self.name, self.buffer))
            for dd in self.buffer.split('\n'):
                self.rx_queue.put(dd.strip())
        if rx == '':
            self.receive = self.buffer
            return True
        elif self.buffer != '' and rx in self.buffer:
            self.receive = self.buffer[self.buffer.rfind(rx):]
            return True
        return False

    def get_char(self, size, timeout=1):
        _start = int(round(time() * 1000))
        _now = int(round(time() * 1000))
        _data = None
        while _now - _start < timeout*10:
            _data = self.port.read(size) or None
            if _data is not None:
                return _data
            else:
                sleep(0.1)
            _now = int(round(time() * 1000))
        return _data

    def put_char(self, data):
        return self.port.write(data)


class ModuleForm(object):
    def __init__(self):
        self.workWidget = QWidget()
        self.workUi = ui_pg.Ui_Form()
        self.workUi.setupUi(self.workWidget)

        self.work_serial = Serial(module_port_id, 9600, 50)

        self.win = pg.GraphicsWindow()
        self.win.resize(600, 400)
        self.workUi.verticalLayout.addWidget(self.win)
        self.plot = self.win.addPlot()
        self.plot.showGrid(x=True, y=True)
        # self.plot.setLabel(axis='left', text='Amplitude / V')
        # self.plot.setLabel(axis='bottom', text='t / s')
        self.plot.setTitle('y1=acc_x y2=acc_y y3=acc_z y4=acc_s')
        # self.plot.addLegend()

        self.curve1 = self.plot.plot(pen='r', name='y1')
        self.curve2 = self.plot.plot(pen='y', name='y2')
        self.curve3 = self.plot.plot(pen='g', name='y3')
        self.curve4 = self.plot.plot(pen='b', name='y4')

        self.num = 100
        self.time = 5
        self.freq = int(self.num / self.time)
        self.x = np.arange(0, self.num, self.time)
        self.y1 = np.full(np.arange(0, self.num, 5).shape, 0)
        self.y2 = np.full(np.arange(0, self.num, 5).shape, 0)
        self.y3 = np.full(np.arange(0, self.num, 5).shape, 0)
        self.y4 = np.full(np.arange(0, self.num, 5).shape, 0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(100)

    def set_data(self, data):
        self.y1[:-1] = self.y1[1:]
        self.y1[-1] = data[0]
        self.y2[:-1] = self.y2[1:]
        self.y2[-1] = data[1]
        self.y3[:-1] = self.y3[1:]
        self.y3[-1] = data[2]
        self.y4[:-1] = self.y4[1:]
        print(data[0])
        print(data[1])
        print(data[2])
        _tmp = int((data[0]*data[0] + data[1]*data[1] + data[2]*data[2]) / 3) ** 0.5
        print(_tmp)
        self.y4[-1] = _tmp
        self.curve1.setData(self.x, self.y1)
        self.curve2.setData(self.x, self.y2)
        self.curve3.setData(self.x, self.y3)
        self.curve4.setData(self.x, self.y4)

    def timer_event(self):
        self.work_serial.set_send('', '')
        while not self.work_serial.rx_queue.empty():
            _data = self.work_serial.rx_queue.get()
            if 'Pressure' in _data:
                _list = _data.split(' ')
                if (len(_list) >= 12) and ('Pressure' in _list[0]) and ('Temperature' in _list[5]) and (
                        'Humidity' in _list[10]):
                    x = _list[1]
                    y = _list[6]
                    z = _list[11]
                    write_log('获取 气压=%s 温度=%s 湿度=%s' % (x, y, z))
            if 'ACC_X' in _data:
                _idx = _data.find('ACC_X')
                _data = _data[_idx:-1]
                _list = _data.split(' ')
                if len(_list) >= 6 and 'ACC_X' in _list[0] and 'ACC_Y' in _list[2] and 'ACC_Z' in _list[4]:
                    x = _list[1].split(',')[0]
                    y = _list[3].split(',')[0]
                    z = _list[5].split('\r')[0]
                    write_log('获取加速器 X=%s Y=%s Z=%s' % (x, y, z))
                    self.set_data((float(x), float(y), float(z)))
            if 'GYR_X' in _data:
                _idx = _data.find('GYR_X')
                _data = _data[_idx:-1]
                _list = _data.split(' ')
                if len(_list) >= 6 and 'GYR_X' in _list[0] and 'GYR_Y' in _list[2] and 'GYR_Z' in _list[4]:
                    x = _list[1].split(',')[0]
                    y = _list[3].split(',')[0]
                    z = _list[5].split('\r')[0]
                    write_log('获取陀螺仪 X=%s Y=%s Z=%s' % (x, y, z))
            if 'MAG_X' in _data:
                _idx = _data.find('MAG_X')
                _data = _data[_idx:-1]
                _list = _data.split(' ')
                if len(_list) >= 6 and 'MAG_X' in _list[0] and 'MAG_Y' in _list[2] and 'MAG_Z' in _list[4]:
                    x = _list[1].split(',')[0]
                    y = _list[3].split(',')[0]
                    z = _list[5].split('\r')[0]
                    write_log('获取三轴磁 X=%s Y=%s Z=%s' % (x, y, z))

    def show(self):
        self.workWidget.show()


def main():
    app = QApplication(sys.argv)
    mf = ModuleForm()
    mf.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
