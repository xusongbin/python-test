#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import queue
import threading
from traceback import format_exc
from time import time, sleep

import serial
from serial.tools import list_ports

from myDriver.hhLog import write_log
from myDriver.hhXmodem import XMODEM


class Serial(object):
    __len = 8
    __parity = serial.PARITY_NONE
    __stop = 1
    __port = serial.Serial()
    __queue_max = 500
    __name = ''
    __timeout = 0.05

    def __init__(self, desc, baud, timeout=300, wakeup=False, byte=False, ignore='', alog=False):
        self.__desc = desc
        self.__baud = baud
        self.__tout = timeout / 1000
        self.__wakeup = wakeup
        self.__byte = byte
        self.__ignore = ignore
        self.__alog = alog
        self.__queue_rx = queue.Queue()
        self.__queue_tx = queue.Queue()
        self.__xmodem = XMODEM(self.__get_char, self.__put_char, mode='xmodem1k')
        self.__xmodem_sta = False
        self.__halt = False
        self.close()

        self.__com_turn = 0

        self.__thread_evt = threading.Thread(target=self.__on_serial_thread)
        self.__thread_evt.setDaemon(True)
        self.__thread_evt.start()

    def xmodem_send(self, path):
        self.__xmodem_sta = True
        try:
            with open(path, 'rb') as f:
                result = self.__xmodem.send(f, timeout=50, retry=20)
        except Exception as e:
            write_log('xmodem send fail:{}\n{}'.format(e, format_exc()))
            result = False
        self.__xmodem_sta = False
        return result

    def xmodem_recv(self, path):
        self.__xmodem_sta = True
        try:
            with open(path, 'wb') as f:
                result = self.__xmodem.recv(f)
            return result
        except Exception as e:
            write_log('xmodem recv fail:{}\n{}'.format(e, format_exc()))
        self.__xmodem_sta = False
        return False

    def xmodem_step(self):
        return self.__xmodem.step

    def xmodem_clear(self):
        self.__xmodem.step = 0

    def __get_char(self, size, timeout=0.001):
        _data = None
        _now = time()
        while (time() - _now) < timeout:
            _data = self.__port.read(size) or None
            if _data:
                break
            else:
                sleep(0.001)
            _now = time()
        print('xmodem1k get:', end='')
        print(_data)
        return _data

    def __put_char(self, data):
        print('xmodem1k put:', end='')
        print(data)
        self.__port.write(data)
        sleep(0.01)

    @staticmethod
    def get_port_to_list():
        _list = []
        try:
            for comport in list_ports.comports():
                name = str(comport)
                name = name.split(' ')[0]
                _list.append(name)
        except Exception as e:
            _ = e
        return _list

    def get_port_by_hid(self, hid):
        _com = []
        try:
            for comport in list_ports.comports():
                if hid in comport.hwid:
                    name = str(comport)
                    name = name.split(' ')[0]
                    _com.append(name)
        except Exception as e:
            _ = e
        if len(_com) == 0:
            return None
        return _com[0]
        # self.__com_turn += 1
        # if self.__com_turn >= len(_com):
        #     self.__com_turn = 0
        # for idx, name in enumerate(_com):
        #     if self.__ignore and self.__ignore == name:
        #         continue
        #     if self.__com_turn > idx:
        #         continue
        #     return name
        # return None

    def set_halt(self, sta):
        self.__halt = sta

    def set_ignore(self, com):
        self.__ignore = com
        self.close()

    def reset_timeout(self, timeout):
        self.__tout = timeout / 1000

    def reset_describe(self, desc):
        self.__desc = desc
        self.close()

    def reset_rate(self, rate):
        self.__baud = rate
        self.close()

    def get_port_name(self):
        try:
            return self.__port.name
        except Exception as e:
            _ = e
        return None

    def get_port_open(self):
        try:
            return self.__port.is_open
        except Exception as e:
            _ = e
        return False

    def clear(self):
        if self.__queue_rx.empty():
            return True
        self.__queue_rx.queue.clear()
        return True

    def get(self, timeout=None):
        if not timeout:
            if self.__queue_rx.empty():
                return ''
            if self.__byte:
                return self.__queue_rx.get()
            else:
                return self.__queue_rx.get().decode('utf-8', 'ignore').strip()
        _start = time()
        while (time() - _start) < timeout/1000:
            sleep(0.005)
            if self.__queue_rx.empty():
                continue
            if self.__byte:
                return self.__queue_rx.get()
            else:
                return self.__queue_rx.get().decode('utf-8', 'ignore').strip()
        return ''

    def roll(self, timeout=None):
        if not timeout:
            timeout = 100
        _start = time()
        while (time() - _start) < timeout / 1000:
            if not self.get():
                sleep(0.005)
                continue
            _start = time()

    def open(self):
        if 'COM' in self.__desc:
            port = self.__desc
        else:
            port = self.get_port_by_hid(self.__desc)
        if not port:
            return False
        try:
            self.__port = serial.Serial(
                port=port,
                baudrate=self.__baud,
                bytesize=self.__len,
                stopbits=self.__stop,
                parity=self.__parity,
                timeout=0)
            if self.__alog and port:
                write_log('open pass:{}'.format(port), 'log_{}.txt'.format(port))
            else:
                write_log('open pass:{}'.format(port))
            return True
        except Exception as e:
            _ = e
            # write_log('open fail:{}\n{}'.format(e, format_exc()))
        return False

    def close(self):
        name = self.get_port_name()
        try:
            self.__port.close()
            if self.__alog and name:
                write_log('close pass:{}'.format(name), 'log_{}.txt'.format(name))
            else:
                write_log('close pass:{}'.format(name))
            return True
        except Exception as e:
            if self.__alog and name:
                write_log('close fail:{}\n{}'.format(e, format_exc()), 'log_{}.txt'.format(name))
            else:
                write_log('close fail:{}\n{}'.format(e, format_exc()))
        return False

    def open_rst(self):
        self.close()
        return self.open()

    def send(self, data, directory=False, Linux=False):
        if not data:
            return True
        name = self.get_port_name()
        if not self.get_port_open():
            return False
        try:
            if directory:
                if self.__wakeup:
                    self.__port.write(b'\xff\xff\xff\xff')
                if type(data) is str:
                    if Linux:
                        data = data.strip() + '\n'
                    else:
                        data = data.strip() + '\r\n'
                    self.__port.write(data.encode('utf-8'))
                else:
                    self.__port.write(data)
                data = data.strip()
                if self.__alog and name:
                    write_log('{} send:{}'.format(name, data), 'log_{}.txt'.format(name))
                else:
                    write_log('{} send:{}'.format(name, data))
            else:
                self.__queue_tx.put(data)
            return True
        except Exception as e:
            if self.__alog and name:
                write_log('{} send except:{}\n{}'.format(name, e, format_exc()), 'log_{}.txt'.format(name))
            else:
                write_log('{} send except:{}\n{}'.format(name, e, format_exc()))
            self.close()
        return False

    def read(self):
        data = b''
        start = time()
        name = self.get_port_name()
        try:
            while (time() - start) <= self.__timeout:
                rx_byte = self.__port.read()
                if not rx_byte:
                    sleep(0.005)
                    continue
                if not self.__byte and (rx_byte == b'\r' or rx_byte == b'\n'):
                    break
                data += rx_byte
                start = time()
            if data:
                if self.__alog and name:
                    write_log('{} read:{}'.format(name, data), 'log_{}.txt'.format(name))
                else:
                    write_log('{} read:{}'.format(name, data))
        except Exception as e:
            if self.__alog and name:
                write_log('{} read except:{}\n{}'.format(name, e, format_exc()), 'log_{}.txt'.format(name))
            else:
                write_log('{} read except:{}\n{}'.format(name, e, format_exc()))
            self.close()
        return data

    def send_wait_re_retry(self, tx, regular=None, tout=None, retry=3, Linux=False):
        while retry:
            retry -= 1
            rx = self.send_wait_regular(tx, regular, tout, Linux)
            if rx:
                return rx
        return False

    def send_wait_regular(self, tx, regular=None, tout=None, Linux=False):
        if tout:
            tout = tout / 1000
        else:
            tout = self.__tout
        self.send(tx, True, Linux)
        start = time()
        while (time() - start) <= tout:
            rx = self.get()
            if rx:
                start = time()
                if self.__byte or not regular:
                    return rx
                elif re.match(regular, rx):
                    return rx
            else:
                sleep(0.005)
        return False

    def recv_wait_send(self, tx, regular=r'.+', tout=None):
        if tout:
            tout = tout / 1000
        else:
            tout = self.__tout
        start = time()
        while (time() - start) <= tout:
            rx = self.get()
            if rx:
                start = time()
                if self.__byte:
                    return rx
                elif re.match(regular, rx):
                    return rx
            else:
                sleep(0.005)
        self.send(tx, True)
        return False

    def __on_serial_thread(self):
        while True:
            if self.__xmodem_sta or self.__halt:
                sleep(0.1)
                continue
            if not self.get_port_open():
                sleep(0.1)
                self.open()
                continue
            if not self.__queue_tx.empty():
                self.send(self.__queue_tx.get(), True)
            line = self.read()
            if not line:
                sleep(0.05)
                continue
            self.__queue_rx.put(line)


if __name__ == '__main__':
    test_ser = Serial('COM55', 9600)
    print(test_ser.get_port_to_list())
