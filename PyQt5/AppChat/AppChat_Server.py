#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from AppChat_Server_ui import *


class TcpS(QWidget):
    sendFileName = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)

        self.message_box = QMessageBox(self)
        self.file_dialog = QFileDialog(self)

        self.wui.pushButtonOpen.clicked.connect(self.on_pb_open_clicked)
        self.wui.pushButtonSend.clicked.connect(self.on_pb_send_clicked)
        self.wui.pushButtonClose.clicked.connect(self.on_pb_close_clicked)
        self.wui.progressBar.reset()
        self.wui.pushButtonOpen.setEnabled(True)
        self.wui.pushButtonSend.setEnabled(False)

        self.payload_size = 64 * 1024
        self.byte_total = 0
        self.byte_writen = 0
        self.byte_to_write = 0
        self.block = 0

        self.file_size = 0
        self.file_name = ''
        self.the_file_name = ''

        self.tcp_port = 7788
        self.tcp_sock = QTcpServer(self)
        self.client_connect = QTcpSocket(self)
        self.tcp_sock.newConnection.connect(self.send_message)
        self.tcp_sock.close()

        self.local_file = QFile()
        self.out_block = QByteArray()

        self.time = QTime()

    def refused(self):
        self.tcp_sock.close()
        self.wui.label.setText('对方拒绝接收')

    def closeEvent(self, e):
        self.on_pb_close_clicked()

    def send_message(self):
        self.wui.pushButtonSend.setEnabled(False)
        self.client_connect = self.tcp_sock.nextPendingConnection()
        self.client_connect.byte_writen.connect(self.updateClientProgress)
        self.wui.pushButtonSend.setText("开始传送文件 {} ！".format(self.theFileName))

        self.local_file = QFile(self.file_name)
        if not (self.local_file.open(QFile.ReadOnly)):
            msg = "无法读取文件 {}:\n {}".format(self.file_name, self.local_file.errorString())
            self.message_box.warning(self, "应用程序", msg)
            return

        self.wui.pushButtonClose.setText("取消")

        self.byte_total = self.local_file.size()  # 单位：字节
        send_out = QDataStream(self.outBlock, QIODevice.WriteOnly)
        send_out.setVersion(QDataStream.Qt_5_4)
        self.time.start()
        current_file = self.file_name.split("/")[-1]
        send_out.writeInt64(0)
        send_out.writeInt64(0)
        send_out.writeQString(current_file)
        self.byte_total += self.outBlock.size()
        send_out.device().seek(0)
        send_out.writeInt64(self.byte_total)
        send_out.writeInt64(self.outBlock.size() - 2)
        self.byte_to_write = self.byte_total - self.client_connect.write(self.outBlock)
        self.outBlock.resize(0)

    def update_client_propress(self, num):
        qApp.processEvents()
        self.byte_writen += num
        if self.byte_writen > 0:
            self.block = self.local_file.read(min(self.bytesToWrite, self.payloadSize))
            self.bytesToWrite -= self.client_connect.write(self.block)
        else:
            self.local_file.close()

        byte_sent = self.byte_writen / (1024 * 1024)
        use_time = self.time.elapsed() / 1000
        speed = self.byte_writen / use_time / (1024 * 1024)
        total = self.byte_total / (1024 * 1024)
        _left = (total - byte_sent) / speed

        if byte_sent < 0.01:
            byte_sent = self.byte_writen / 1024
            speed = self.byte_writen / use_time / 1024
            total = self.byte_total / 1024
            if _left > 0:
                msg = "已发送 {0:.2f}KB（{1:.2f}KB/s)\n共{2:.2f}KB 已用时：{3:.1f}秒\n 估计剩余时间:{4:.1f}秒".format(
                    byte_sent, speed, total, use_time, _left
                )
            else:
                msg = "已发送 {0:.2f}KB（{1:.2f}KB/s)\n共{2:.2f}KB 用时：{3:.1f}秒\n".format(
                    byte_sent, speed, total, use_time
                )
        else:
            if _left > 0:
                msg = "已发送 {0:.2f}MB（{1:.2f}MB/s)\n共{2:.2f}MB 已用时：{3:.1f}秒\n 估计剩余时间:{4:.1f}秒".format(
                    byte_sent, speed, total, use_time, _left
                )
            else:
                msg = "已发送 {0:.2f}MB（{1:.2f}MB/s)\n共{2:.2f}MB 用时：{3:.1f}秒\n".format(
                    byte_sent, speed, total, use_time
                )
        self.wui.progressBar.setMaximum(total)
        self.wui.progressBar.setValue(byte_sent)

        if self.byte_writen == self.byte_total:
            self.wui.pushButtonClose.setText("关闭")

        self.wui.label.setText(msg)

    def on_pb_open_clicked(self):
        self.file_name = self.file_dialog.getOpenFileName(self, '打开文件', './')[0]
        if self.file_name:
            self.the_file_name = self.file_name.split("/")[-1]
            self.wui.label.setText("要传送的文件为：{}".format(self.the_file_name))
            self.wui.pushButtonSend.setEnabled(True)
            self.wui.pushButtonOpen.setEnabled(False)

    def on_pb_send_clicked(self):
        if not (self.tcp_sock.listen(QHostAddress.Any, self.tcp_port)):
            msg = self.tcp_sock.errorString()
            self.message_box.warning(self, "错误", "发送失败：\n {}".format(msg))
            self.tcp_sock.close()
            return
        self.wui.label.setText("等待对方接收... ...")
        self.wui.pushButtonSend.setEnabled(False)
        self.sendFileName.emit(self.the_file_name)

    def on_pb_close_clicked(self):
        if self.tcp_sock.isListening():
            self.tcp_sock.close()
            if self.local_file.isOpen():
                self.local_file.close()
            self.client_connect.abort()
        if self.wui.pushButtonClose.text() == "取消":
            self.wui.pushButtonClose.setText("关闭")
        else:
            self.close()
            self.wui.pushButtonOpen.setEnabled(True)
            self.wui.pushButtonSend.setEnabled(False)
            self.wui.progressBar.reset()
            self.byte_total = 0
            self.byte_writen = 0
            self.byte_to_write = 0
            self.wui.label.setText("请选择要传送的文件")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = TcpS()
    exe.show()
    sys.exit(app.exec_())
