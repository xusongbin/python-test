#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from AppChat_Client_ui import *


class TcpC(QWidget):
    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)

        self.message_box = QMessageBox(self)

        self.wui.pushButtonClose.clicked.connect(self.on_pb_close_clicked)
        self.wui.pushButtonCancel.clicked.connect(self.on_pb_cancel_clicked)

        self.byte_total = 0
        self.byte_receive = 0
        self.byte_to_receive = 0

        self.file_size = 0
        self.file_name = ''

        self.tcp_sock = QTcpSocket(self)
        self.tcp_port = 7788

        self.host_addr = ''
        self.local_file = QFile()

        self.time = QTime()

        self.tcp_sock.readyRead.connect(self.read_message)
        self.tcp_sock.error.connect(self.display_error)

    def set_host_addr(self, addr):
        self.host_addr = addr
        self.new_connect()

    def set_filename(self, filename):
        self.local_file = QFile(filename)

    def closeEvent(self, e):
        self.on_pb_close_clicked()

    def new_connect(self):
        self.tcp_sock.abort()
        self.tcp_sock.connectToHost(self.host_addr, self.tcp_port)
        self.time.start()

    def read_message(self):
        receiver = QDataStream(self.tcp_sock)
        if self.byte_receive <= 2:
            if self.tcp_sock.bytesAvailable() >= 2 and self.file_size == 0:
                self.byte_total = receiver.readInt64()
                self.file_size = receiver.readInt64()
                self.byte_receive += 2
            if self.tcp_sock.bytesAvailable() >= self.file_size != 0:
                self.file_name = receiver.readQString()
                self.byte_receive += self.file_size
                if not (self.localFile.open(QFile.WriteOnly)):
                    self.message_box.warning(
                        self, "应用程序", "无法读取文件 {}：\n {}".format(self.file_name, self.local_file.errorString())
                    )
                    return
            else:
                return

        if self.byte_receive < self.byte_total:
            self.byte_receive += self.tcp_sock.bytesAvailable()
            block = self.tcp_sock.readAll()
            self.local_file.write(block)
            block.resize(0)
        use_time = self.time.elapsed() / 1000
        _byte_received = self.byte_receive / (1024 * 1024)
        speed = _byte_received / use_time
        total = self.byte_total / (1024 * 1024)
        _left = (total - _byte_received) / speed

        if _byte_received < 0.01:
            _byte_received = self.bytesReceive / 1024
            speed = _byte_received / use_time / 1024
            total = self.TotalBytes / 1024
            if _left > 0:
                msg = "已接收 {0:.2f} KB ({1:.2f}KB/s)\n共{2:.2f}KB.已用时：{3:.1f}秒\n估计剩余时间：{4:.1f}秒".format(
                    _byte_received, speed, total, use_time, _left
                )
            else:
                msg = "已接收 {0:.2f} KB ({1:.2f}KB/s)\n共{2:.2f}KB.已用时：{3:.1f}秒\n".format(
                    _byte_received, speed, total, use_time
                )
        else:
            if _left > 0:
                msg = "已接收 {0:.2f} MB ({1:.2f}MB/s)\n共{2:.2f}MB.已用时：{3:.1f}秒\n估计剩余时间：{4:.1f}秒".format(
                    _byte_received, speed, total, use_time, _left
                )
            else:
                msg = "已接收 {0:.2f} MB ({1:.2f}MB/s)\n共{2:.2f}MB.已用时：{3:.1f}秒\n".format(
                    _byte_received, speed, total, use_time
                )
        self.wui.progressBar.setMaximum(total)
        self.wui.progressBar.setValue(_byte_received)
        self.wui.label.setText(msg)
        if self.byte_receive == self.byte_total:
            self.local_file.close()
            self.tcp_sock.close()
            self.wui.label.setText("接收文件{}完毕".format(self.fileName))
            self.wui.pushButtonCancel.setEnabled(False)

    def display_error(self, err):
        if err == QAbstractSocket.RemoteHostClosedError:
            pass
        else:
            msg = self.tcp_sock.errorString()
            self.message_box.warning(self, "应用程序", msg)
            return

    def on_pb_cancel_clicked(self):
        self.tcp_sock.abort()
        if self.local_file.isOpen():
            self.local_file.close()
        self.wui.pushButtonCancel.setEnabled(False)

    def on_pb_close_clicked(self):
        self.tcp_sock.abort()
        if self.local_file.isOpen():
            self.local_file.close()
        self.wui.pushButtonCancel.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = TcpC()
    exe.show()
    sys.exit(app.exec_())
