#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import traceback
from queue import Queue
from time import sleep, time

import serial
from serial.tools import list_ports


class ThreadSerial(object):
    def __init__(
            self,
            baudrate=115200, byte=8, parity=serial.PARITY_NONE, stopbits=1,
            com='', hid='', thread=True, period=0.1, timeout=0.02, qqlen=50, enter=False, wakeup=False
    ):
        self.baudrate = baudrate
        self.byte = byte
        self.parity = parity
        self.stopbits = stopbits
        self.port = serial.Serial()

        self.serial_hid = hid
        self.serial_com = com

        self.enter = enter
        self.wakeup = wakeup
        self.thread = thread
        self.period = period
        self.timeout = timeout

        self.qq_tx = Queue()
        self.qq_rx = Queue()
        self.qq_len = qqlen

        self.open()

        if self.thread:
            self.serial_thread = threading.Thread(target=self.on_serial_thread)
            self.serial_thread.setDaemon(True)
            self.serial_thread.start()

    @staticmethod
    def serial_list():
        _list = []
        try:
            for _describe in list_ports.comports():
                _list.append(str(_describe).split('-')[0].strip())
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        return _list

    @staticmethod
    def find_by_hid(hid):
        if not hid:
            return ''
        try:
            for _describe in list_ports.comports():
                if hid in _describe.hwid:
                    return str(_describe).split('-')[0].strip()
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        return ''

    def close(self):
        try:
            if self.port.isOpen():
                self.port.close()
            return True
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        return False

    def open(self, com='', hid=''):
        if not com:
            if not hid:
                # print('ThreadSerial open: No describe!')
                return False
            com = self.find_by_hid(hid)
        if not com:
            # print('ThreadSerial open: No found hid!')
            return False
        try:
            self.port = serial.Serial(
                port=com,
                baudrate=self.baudrate,
                bytesize=self.byte,
                stopbits=self.stopbits,
                parity=self.parity,
                timeout=0)
            print('ThreadSerial open: successful!')
            return True
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        return False

    def send(self, tx, clear=False):
        try:
            if clear:
                self.qq_tx.queue.clear()
            self.qq_tx.put(tx)
            return True
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        return False

    def receive(self, onerow=False, clear=False):
        try:
            rx_str = ''
            while not self.qq_rx.empty():
                rx_str += self.qq_rx.get() + '\n'
                if onerow:
                    if clear:
                        self.qq_rx.queue.clear()
                    return rx_str
            return rx_str
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        return ''

    def send_wait(self, tx, timeout):
        rx_str = ''
        if not self.port.isOpen():
            self.open(self.serial_com, self.serial_hid)
            if not self.port.isOpen():
                return rx_str
        if self.enter:
            tx = str(tx).strip() + '\r\n'
        try:
            if self.wakeup:
                self.port.write(b'\xff\xff\xff\xff')
            self.port.write(tx.encode('utf-8', 'ignore'))
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        try:
            rx_ts = time()
            while (time() - rx_ts) < timeout:
                rx_byte = self.port.read()
                if not rx_byte:
                    break
                rx_str += rx_byte.decode("utf-8", "ignore")
                rx_ts = time()
        except Exception as e:
            print('{}\n{}'.format(e, traceback.format_exc()))
        rx_str = rx_str.strip()
        return rx_str

    def on_serial_thread(self):
        while self.thread:
            if not self.port.isOpen():
                self.open(self.serial_com, self.serial_hid)
                continue
            if not self.qq_tx.empty():
                tx = self.qq_tx.get()
                if self.enter:
                    tx = str(tx).strip()+'\r\n'
                try:
                    if self.wakeup:
                        self.port.write(b'\xff\xff\xff\xff')
                    self.port.write(tx.encode('utf-8', 'ignore'))
                except Exception as e:
                    print('{}\n{}'.format(e, traceback.format_exc()))
            try:
                rx_line = ''
                rx_ts = time()
                while (time() - rx_ts) < self.timeout:
                    rx_byte = self.port.read()
                    if not rx_byte:
                        break
                    if rx_byte == b'\n':
                        break
                    rx_line += rx_byte.decode("utf-8", "ignore")
                    rx_ts = time()
                rx_line = rx_line.strip()
                if rx_line:
                    self.qq_rx.put(rx_line)
            except Exception as e:
                print('{}\n{}'.format(e, traceback.format_exc()))
            while self.qq_tx.qsize() > self.qq_len:
                self.qq_tx.get()
            while self.qq_rx.qsize() > self.qq_len:
                self.qq_rx.get()
            sleep(self.period)


if __name__ == '__main__':
    from time import strftime, localtime
    ser = ThreadSerial(hid='VID:PID=0483:5740', enter=True, thread=False)
    ser.receive()
    while True:
        sleep(1)
        # ser.send('AT')
        # print('{}:{}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()), 'AT'))
        rx = ser.send_wait('AT', 0.1)
        if rx:
            print('{}:{}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()), rx))
