
# 局域网聊天工具

import os
import sys
import json
import codecs
import pickle
import random

from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AppChat_ui import *
from AppChat_Client import TcpC
from AppChat_Server import TcpS


class Chat(QWidget):
    Message, NewParticipant, ParticipantLeft, FileName, Refuse = range(5)

    def __init__(self):
        super().__init__()

        self.wui = Ui_Form()
        self.wui.setupUi(self)

        self.wui.tableWidget.setColumnWidth(0, 50)
        self.wui.tableWidget.setColumnWidth(1, 90)
        self.wui.tableWidget.setColumnWidth(2, 90)
        self.wui.fontComboBox.currentTextChanged.connect(self.on_cb_font_changed)
        self.wui.sizeComboBox.currentTextChanged.connect(self.on_cb_size_changed)
        self.wui.toolButtonBold.clicked.connect(self.on_tb_bold_clicked)
        self.wui.toolButtonItalic.clicked.connect(self.on_tb_italic_clicked)
        self.wui.toolButtonUnderline.clicked.connect(self.on_tb_underline_clicked)
        self.wui.toolButtonColor.clicked.connect(self.on_tb_color_clicked)
        self.wui.toolButtonSave.clicked.connect(self.on_tb_save_clicked)
        self.wui.toolButtonSend.clicked.connect(self.on_tb_send_clicked)
        self.wui.toolButtonClear.clicked.connect(self.on_tb_clear_clicked)
        self.wui.pushButtonSend.clicked.connect(self.on_pb_send_clicked)
        self.wui.pushButtonExit.clicked.connect(self.on_pb_exit_clicked)

        self.message_box = QMessageBox(self)
        self.file_dialog = QFileDialog(self)
        self.log = True

        self.udp_sock = None
        self.udp_port = 0
        self.filename = ''
        self.server = TcpS()
        self.server.sendFileName.connect(self.get_filename)
        self.network_init()

    def network(self):
        self.udp_sock = QUdpSocket(self)
        self.udp_port = 12345
        self.udp_sock.bind(self.udp_port, QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint)
        self.udp_sock.readyRead.connect(self.process_pending_data)

    def network_init(self):
        self.network()
        self.send_message(Chat.NewParticipant)
        _title = '微信公众号：局域网聊天小工具 | 当前用户：{} | IP：{}'.format(self.get_username(), self.get_ip())
        self.setWindowTitle(_title)

    def new_client(self, user_name, local_host, ip_addr):
        is_empty = self.wui.tableWidget.findItems(ip_addr, Qt.MatchExactly)
        if not is_empty:
            self.wui.tableWidget.insertRow(0)
            self.wui.tableWidget.setItem(0, 0, QTableWidgetItem(user_name))
            self.wui.tableWidget.setItem(0, 1, QTableWidgetItem(local_host))
            self.wui.tableWidget.setItem(0, 2, QTableWidgetItem(ip_addr))

            self.wui.textBrowser.setTextColor(Qt.gray)
            self.wui.textBrowser.setCurrentFont(QFont("Times New Roman", 10))
            self.wui.textBrowser.append('{}在线'.format(user_name))
            self.wui.labelUserNum.setText('{}'.format(self.wui.tableWidget.rowCount()))
            self.send_message(Chat.NewParticipant)

    def client_left(self, user_name, ip_addr, time):
        find_item = self.wui.tableWidget.findItems(ip_addr, Qt.MatchExactly)
        if find_item:
            self.wui.tableWidget.removeRow(find_item[0].row())
            self.wui.textBrowser.setTextColor(Qt.gray)
            self.wui.textBrowser.setCurrentFont(QFont("Times New Roman", 10))
            self.wui.textBrowser.append('{}于{}离开!'.format(user_name, time))
            self.wui.labelUserNum.setText('{}'.format(self.wui.tableWidget.rowCount()))

    def save_file(self, file_name):
        file_type = file_name.split('.')[1]
        if file_type in ['htm', 'html']:
            content = self.wui.textBrowser.toHtml()
        else:
            content = self.wui.textBrowser.toPlainText()
        try:
            with codecs.open(file_name, 'w', encoding='gbk') as f:
                f.write(content)
            return True
        except IOError:
            self.message_box.critical(self, '保存错误', '聊天记录保存失败！')
            return False

    def closeEvent(self, e):
        self.send_message(Chat.ParticipantLeft)

    def has_pending_file(self, user, server, client, file):
        ip = self.get_ip()
        if ip == client:
            msg = '来自{}({})的文件：{}，是否接收？'.format(user, server, file)
            btn = self.message_box.information(self, '接收文件', msg, QMessageBox.Yes | QMessageBox.No)
            if btn == QMessageBox.Yes:
                name = self.file_dialog.getSaveFileName(self, '保存文件', file)
                if name[0]:
                    client = TcpC()
                    client.set_file_name(name[0])
                    client.set_host_addr(QHostAddress(server))
                    client.exec()
            else:
                self.send_message(Chat.Refuse, server)
                self.udp_sock.close()
                self.network()

    def process_pending_data(self):
        while self.udp_sock.hasPendingDatagrams():
            data, host, port = self.udp_sock.readDatagram(self.udp_sock.pendingDatagramSize())
            data = str(data, encoding='utf-8')
            data_dict = json.loads(data)

            msg_type = data_dict['messageType']
            user_name = data_dict['userName']
            local_host = data_dict['localHostName']
            ip_addr = data_dict['ipAddress']

            time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')

            if msg_type == Chat.Message:
                message = data_dict['message']
                if self.find_at(message) == self.get_username():
                    QApplication.alert(self, 0)
                self.wui.textBrowser.setTextColor(Qt.blue)
                self.wui.textBrowser.setCurrentFont(QFont("Times New Roman", 12))
                self.wui.textBrowser.append('[{}]{}'.format(user_name, time))
                self.wui.textBrowser.append(message)
            elif msg_type == Chat.NewParticipant:
                self.new_client(user_name, local_host, ip_addr)
            elif msg_type == Chat.ParticipantLeft:
                self.client_left(user_name, ip_addr, time)
            elif msg_type == Chat.FileName:
                client = data_dict['clientAddress']
                filename = data_dict['sendFileName']
                self.has_pending_file(user_name, ip_addr, client, filename)
            elif msg_type == Chat.Refuse:
                if ip_addr == self.get_ip():
                    self.server.refused()
            QApplication.processEvents()

    def get_filename(self, name):
        self.filename = name
        self.send_message(Chat.FileName)

    def find_at(self, msg):
        for row in range(self.wui.tableWidget.rowCount()):
            username = self.wui.tableWidget.item(row, 0).text()
            at_username = '@' + username
            if msg.find(at_username) >= 0:
                return username
        return 'NotFound'

    def send_message(self, msg_type, server=''):
        local_host = QHostInfo.localHostName()
        ip_addr = self.get_ip()
        username = self.get_username()
        data = {"messageType": msg_type, "userName": username, "localHostName": local_host}

        if msg_type == Chat.Message:
            if self.wui.textEdit.toPlainText() == '':
                self.message_box.warning(self, '警告', '发送内容不能为空', QMessageBox.Ok)
                return
            message = self.get_message()
            data['ipAddress'] = ip_addr
            data['message'] = message
        elif msg_type in [Chat.NewParticipant, Chat.ParticipantLeft]:
            data['ipAddress'] = ip_addr
        elif msg_type == Chat.FileName:
            row = self.wui.tableWidget.currentRow()
            client_addr = self.wui.tableWidget.item(row, 2).text()
            data['ipAddress'] = ip_addr
            data['clientAddress'] = client_addr
            data['sendFileName'] = self.filename
        elif msg_type == Chat.Refuse:
            data['ipAddress'] = server

        jdata = json.dumps(data)
        edata = bytes(jdata, encoding='utf-8')

        self.udp_sock.writeDatagram(edata, QHostAddress.Broadcast, self.udp_port)

    def get_ip(self):
        if self.log:
            pass
        for addr in QNetworkInterface.allAddresses():
            if addr.protocol() == QAbstractSocket.IPv4Protocol and \
                    addr != QHostAddress.LocalHost and \
                    addr.toString()[:3] != '169' and \
                    addr.toString().split('.')[-1] != '1':
                return addr.toString()
        return '0.0.0.0'

    def get_message(self):
        msg = self.wui.textEdit.toHtml()
        self.wui.textEdit.clear()
        self.wui.textEdit.setFocus()
        return msg

    def get_username(self):
        if self.log:
            pass
        for var in QProcess.systemEnvironment():
            var_list = var.split('=')
            if var_list[0] in ['USERNAME', 'USER', 'HOSTNAME', 'DOMAINNAME']:
                return var_list[1]
        return 'unKnow'

    def merge_format(self, _format):
        cursor = self.wui.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(_format)
        self.wui.textEdit.mergeCurrentCharFormat(_format)

    def contextMenuEvent(self, e):
        if self.wui.tableWidget.selectedItems():
            select_name = self.wui.tableWidget.selectedItems()[0].text()
            if select_name != self.get_username():
                _menu = QMenu(self)
                _contact = QAction('@TA', self.userTableWidget)
                _menu.addAction(_contact)
                _menu.popup(self.mapToGlobal(e.pos()))
                _contact.triggered.connect(lambda: self.contact_ta(select_name))

    def contact_ta(self, username):
        user_at = "<font color=\'#FF0000\' size='5'>@{} </font>".format(username)
        self.wui.textEdit.append(user_at)
        self.wui.textEdit.setFocus()

    def on_cb_font_changed(self, p):
        fmt = QTextCharFormat()
        fmt.setFontFamily(p)
        self.merge_format(fmt)
        self.wui.textEdit.setFocus()

    def on_cb_size_changed(self, p):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(int(p))
        self.merge_format(fmt)
        self.wui.textEdit.setFocus()

    def on_tb_bold_clicked(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontWeight(checked and QFont.Bold or QFont.Normal)
        self.merge_format(fmt)
        self.wui.textEdit.setFocus()

    def on_tb_italic_clicked(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.merge_format(fmt)
        self.wui.textEdit.setFocus()

    def on_tb_underline_clicked(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.merge_format(fmt)
        self.wui.textEdit.setFocus()

    def on_tb_color_clicked(self):
        col = QColorDialog.getColor(self.wui.textEdit.textColor(), self)
        if not col.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.merge_format(fmt)
        self.wui.textEdit.setFocus()

    def on_tb_save_clicked(self):
        if self.wui.textBrowser.document().isEmpty():
            self.message_box.warning(self, "警告", "聊天记录为空,无法保存!", QMessageBox.Ok)
        else:
            filename = self.file_dialog.getSaveFileName(
                self, "保存聊天记录", "./聊天记录", "ODT files (*.odt);;HTML-Files (*.htm *.html)"
            )
            if filename[0]:
                if self.save_file(filename[0]):
                    self.message_box.information(self, "聊天记录保存", "保存成功！")

    def on_tb_send_clicked(self):
        user_list = self.wui.tableWidget.selectedItems()
        if not user_list:
            self.message_box.warning(self, "选择用户", "请先从用户列表选择要传送的用户!", QMessageBox.Ok)
            return
        row = user_list[0].row()
        if self.wui.tableWidget.item(row, 2).text() == self.get_ip():
            self.message_box.information(self, "提示", "不能发给自己哦！")
        else:
            self.server.exec()

    def on_tb_clear_clicked(self):
        self.wui.textBrowser.clear()

    def on_pb_send_clicked(self):
        self.send_message(Chat.Message)

    def on_pb_exit_clicked(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Chat()
    exe.show()
    sys.exit(app.exec_())
