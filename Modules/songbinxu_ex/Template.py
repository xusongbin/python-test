#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from DFU_Plus_Driver import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DFU_Plus_ui import Ui_Dialog

VERSION = '0.1.1'
module_hid = 'VID:PID=0403:6001'

TST_STA_IDLE = 0
TST_STA_FILE = 1
TST_STA_NORMAL = 2
TST_STA_DFU = 3
TST_STA_UPGRADE = 4
TST_STA_END = 5

TST_SUB_STA_0 = 0
TST_SUB_STA_1 = 1
TST_SUB_STA_2 = 2
TST_SUB_STA_3 = 3
TST_SUB_STA_4 = 4
TST_SUB_STA_5 = 5
TST_SUB_STA_6 = 6


class WorkTest(object):
    def __init__(self):
        self.S_main = TST_STA_IDLE
        self.S_sub = TST_SUB_STA_0

        self.D_err = 0


class ModuleForm(QDialog):
    def __init__(self):
        super().__init__()
        self.work_test = WorkTest()
        self.work_serial = Serial(module_hid, 9600, 500, wakeup=True)
        self.work_firmware = ''

        self.work_bar_total = 100
        self.work_bar_cur = 0
        self.work_bar_per = 0
        self.work_tick_cur = 0
        self.work_tick_tms = 0
        self.work_tick_per = 0

        self.work_text_qq = queue.Queue()
        self.work_text_cls = False
        self.work_mess_dialog = QMessageBox(self)
        self.work_file_dialog = QFileDialog(self)
        self.work_serial_list = []

        self.work_ui = Ui_Dialog()
        self.work_ui.setupUi(self)
        self.setWindowTitle('DFU_Plus')
        self.do_init_ui()

        self.work_timer_ui = QTimer()
        self.work_timer_ui.timeout.connect(self.on_timer_ui)
        self.work_timer_ui.start(50)
        self.work_timer_tick = QTimer()
        self.work_timer_tick.timeout.connect(self.on_timer_tick)
        self.work_timer_tick.start(10)
        self.work_thread_logic = threading.Thread(target=self.on_thread_logic)
        self.work_thread_logic.setDaemon(True)
        self.work_thread_logic.start()

        self.show()

    def do_init_ui(self):
        self.work_ui.toolButton.clicked.connect(self.on_btn_clicked_choose)
        self.work_ui.pushButton.clicked.connect(self.on_btn_clicked_start)
        self.work_ui.comboBoxCom.currentTextChanged.connect(self.on_combo_changed_com)

    def do_display_text(self, msg, cls=False):
        if cls:
            self.work_text_cls = cls
        self.work_text_qq.put(msg)

    def on_btn_clicked_choose(self):
        path = self.work_file_dialog.getOpenFileName(self, 'Open File', './', 'hex Files (*.ebin.bin)')
        if path[0]:
            self.work_firmware = path[0]
            self.work_ui.lineEditFw.setText(path[0])

    def on_btn_clicked_start(self):
        if self.work_test.S_main == TST_STA_IDLE:
            self.logic_sta_next()

    def on_combo_changed_com(self):
        _text = self.work_ui.comboBoxCom.currentText()
        self.work_serial.reset_describe(_text)

    def on_timer_ui(self):
        _current = self.work_serial.xmodem_step()
        if _current != self.work_bar_cur:
            self.work_bar_cur = _current
            _step = _current * 100 / self.work_bar_total
            self.work_ui.progressBar.setValue(int(_step))

        if self.work_text_cls:
            self.work_text_cls = False
            self.work_ui.plainTextEdit.setPlainText('')
        if not self.work_text_qq.empty():
            _text = self.work_text_qq.get()
            write_log('text:{}'.format(_text))
            self.work_ui.plainTextEdit.appendPlainText(_text)

    def on_timer_tick(self):
        self.work_tick_tms += 1
        if self.work_tick_tms >= 100:
            self.work_tick_tms = 0
            self.work_tick_cur += 1

    def do_refresh_serial(self):
        _list = self.work_serial.get_port_to_list()
        if self.work_serial_list != _list:
            self.work_serial_list = _list
            self.work_ui.comboBoxCom.clear()
            self.work_ui.comboBoxCom.addItem('')
            for com in _list:
                self.work_ui.comboBoxCom.addItem(com)
        if self.work_serial.get_port_open():
            if self.work_serial.get_port_name() not in _list:
                self.work_serial.close()
            else:
                self.work_ui.comboBoxCom.setCurrentText(self.work_serial.get_port_name())

    def on_thread_logic(self):
        while True:
            sleep(0.002)
            self.do_refresh_serial()

    def logic_sta_next(self, sta=None):
        if sta == 'IDLE':
            self.work_test.S_main = TST_STA_IDLE
        elif sta == 'ERROR':
            self.work_test.D_err = -self.work_test.S_main
            self.work_test.S_main = TST_STA_END
        else:
            self.work_test.S_main += 1
        if self.work_test.S_main == TST_STA_IDLE:
            self.work_test.D_err = 0
        elif self.work_test.S_main == TST_STA_IDLE + 1:
            self.do_display_text('', True)
        elif self.work_test.S_main > TST_STA_END:
            self.work_test.S_main = TST_STA_IDLE
        write_log('logic: {}'.format(self.work_test.S_main))
        self.work_test.S_sub = TST_SUB_STA_0
        self.work_tick_cur = 0
        self.work_tick_per = 0
        self.work_tick_tms = 0


if __name__ == '__main__':
    write_log('VERSION:{}'.format(VERSION))
    app = QApplication(sys.argv)
    work = ModuleForm()
    sys.exit(app.exec_())
