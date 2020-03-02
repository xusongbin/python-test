#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyperclip
from tkinter import *

from my_driver import *
from history_parse import ParseFile
from north_fetch import North
from ccl import Ccl


class Layout(object):
    def __init__(self, win):
        assert isinstance(win, Tk)
        self.win = win
        self.win.title('test')
        self.win.geometry('600x380')

        self.label_time = Label(self.win, text='数据时间', anchor="w")
        self.label_time.place(x=120, y=20, width=130, height=20)
        self.lable_data = Label(self.win, text='数据内容', anchor="w")
        self.lable_data.place(x=270, y=20, width=150, height=20)
        # self.lable_back = Label(self.win, text='备注', anchor="w")
        # self.lable_back.place(x=420, y=20, width=150, height=20)
        self.lable_info = Label(self.win, text='', anchor="w")
        self.lable_info.place(x=0, y=340, width=300, height=20)

        self.label_1A0001_name = Label(self.win, text='上证指数', anchor="e")
        self.label_1A0001_name.place(x=0, y=60, width=100, height=20)
        self.label_1A0001_time = Label(self.win, text='', anchor="w")
        self.label_1A0001_time.place(x=120, y=60, width=130, height=20)
        self.label_1A0001_data = Label(self.win, text='0', anchor="w")
        self.label_1A0001_data.place(x=270, y=60, width=150, height=20)

        self.label_881155_name = Label(self.win, text='银行指数', anchor="e")
        self.label_881155_name.place(x=0, y=100, width=100, height=20)
        self.label_881155_time = Label(self.win, text='', anchor="w")
        self.label_881155_time.place(x=120, y=100, width=130, height=20)
        self.label_881155_data = Label(self.win, text='0', anchor="w")
        self.label_881155_data.place(x=270, y=100, width=150, height=20)

        self.label_399001_name = Label(self.win, text='深证成指', anchor="e")
        self.label_399001_name.place(x=0, y=140, width=100, height=20)
        self.label_399001_time = Label(self.win, text='', anchor="w")
        self.label_399001_time.place(x=120, y=140, width=130, height=20)
        self.label_399001_data = Label(self.win, text='0', anchor="w")
        self.label_399001_data.place(x=270, y=140, width=150, height=20)

        self.label_NORTH_name = Label(self.win, text='北向资金', anchor="e")
        self.label_NORTH_name.place(x=0, y=180, width=100, height=20)
        self.label_NORTH_time = Label(self.win, text='', anchor="w")
        self.label_NORTH_time.place(x=120, y=180, width=130, height=20)
        self.label_NORTH_data = Label(self.win, text='0', anchor="w")
        self.label_NORTH_data.place(x=270, y=180, width=150, height=20)

        self.label_1A0001_value_name = Label(self.win, text='上证成交额', anchor="e")
        self.label_1A0001_value_name.place(x=0, y=220, width=100, height=20)
        self.label_1A0001_value_time = Label(self.win, text='', anchor="w")
        self.label_1A0001_value_time.place(x=120, y=220, width=130, height=20)
        self.label_1A0001_value_data = Label(self.win, text='0', anchor="w")
        self.label_1A0001_value_data.place(x=270, y=220, width=150, height=20)

        self.label_399001_value_name = Label(self.win, text='深圳成交额', anchor="e")
        self.label_399001_value_name.place(x=0, y=260, width=100, height=20)
        self.label_399001_value_time = Label(self.win, text='', anchor="w")
        self.label_399001_value_time.place(x=120, y=260, width=130, height=20)
        self.label_399001_value_data = Label(self.win, text='0', anchor="w")
        self.label_399001_value_data.place(x=270, y=260, width=150, height=20)

        self.label_ccl_name = Label(self.win, text='持仓量', anchor="e")
        self.label_ccl_name.place(x=0, y=300, width=100, height=20)
        self.label_ccl_time = Label(self.win, text='', anchor="w")
        self.label_ccl_time.place(x=120, y=300, width=130, height=20)
        self.label_ccl_data = Label(self.win, text='0', anchor="w")
        self.label_ccl_data.place(x=270, y=300, width=150, height=20)


class App(object):
    def __init__(self):
        self.win = Tk()
        self.win_ui = Layout(self.win)
        self.win_parse = ParseFile()
        self.win_north = North()
        self.win_ccl = Ccl()

        self.var_info_ts = 0

        self.do_init_win_ui()

        self.thread_win_ui_tick = threading.Thread(target=self.thread_win_ui_tick_event)
        self.thread_win_ui_tick.setDaemon(True)
        self.thread_win_ui_tick.start()

        self.thread_win_ui_logic = threading.Thread(target=self.thread_win_ui_logic_event)
        self.thread_win_ui_logic.setDaemon(True)
        self.thread_win_ui_logic.start()

        self.win.mainloop()

    def do_init_win_ui(self):
        self.win_ui.label_1A0001_data.bind('<Button-1>', self.on_label_1a0001_data_click)
        self.win_ui.label_399001_data.bind('<Button-1>', self.on_label_399001_data_click)
        self.win_ui.label_881155_data.bind('<Button-1>', self.on_label_881155_data_click)
        self.win_ui.label_NORTH_data.bind('<Button-1>', self.on_label_north_data_click)
        self.win_ui.label_1A0001_value_data.bind('<Button-1>', self.on_label_1a0001_value_data_click)
        self.win_ui.label_399001_value_data.bind('<Button-1>', self.on_label_399001_value_data_click)
        self.win_ui.label_ccl_data.bind('<Button-1>', self.on_label_ccl_data_click)

    def do_show_info(self, msg):
        write_log(msg)
        self.win_ui.lable_info['text'] = msg
        self.var_info_ts = 15

    def on_label_1a0001_data_click(self, e):
        try:
            _data = self.win_parse.parse_1a0001(2)[0]
            _show = '{:.1f}'.format(int(_data[-1])/10000)
            self.win_ui.label_1A0001_time['text'] = _data[0]
            self.win_ui.label_1A0001_data['text'] = _show
            pyperclip.copy(_show)
            self.do_show_info('上证指数 复制成功 {}'.format(_show))
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_399001_data_click(self, e):
        try:
            _data = self.win_parse.parse_399001(2)[0]
            _show = '{:.1f}'.format(int(_data[-1])/10000)
            self.win_ui.label_399001_time['text'] = _data[0]
            self.win_ui.label_399001_data['text'] = _show
            pyperclip.copy(_show)
            self.do_show_info('深证成指 复制成功 {}'.format(_show))
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_881155_data_click(self, e):
        try:
            _data = self.win_parse.parse_881155(2)[0]
            _show = '{:.2f}'.format(int(_data[-1])/10000)
            self.win_ui.label_881155_time['text'] = _data[0]
            self.win_ui.label_881155_data['text'] = _show
            pyperclip.copy(_show)
            self.do_show_info('银行指数 复制成功 {}'.format(_show))
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_north_data_click(self, e):
        try:
            _data = self.win_north.get()
            _text = '{}\t{}\t{}'.format(_data[1], _data[2], _data[3])
            self.win_ui.label_NORTH_time['text'] = _data[0]
            self.win_ui.label_NORTH_data['text'] = _text
            pyperclip.copy(_text)
            self.do_show_info('北向资金 复制成功 {}'.format(_text))
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_1a0001_value_data_click(self, e):
        try:
            _data = self.win_parse.parse_1a0001_value()
            _show = '{:.1f}'.format(_data[1]/100000000)
            self.win_ui.label_1A0001_value_time['text'] = _data[0]
            self.win_ui.label_1A0001_value_data['text'] = _show
            pyperclip.copy(_show)
            self.do_show_info('上证成交额 复制成功 {}'.format(_show))
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_399001_value_data_click(self, e):
        try:
            _data = self.win_parse.parse_399001_value()
            _show = '{:.1f}'.format(_data[1]/100000000)
            self.win_ui.label_399001_value_time['text'] = _data[0]
            self.win_ui.label_399001_value_data['text'] = _show
            pyperclip.copy(_show)
            self.do_show_info('深证成交额 复制成功 {}'.format(_show))
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_ccl_data_click(self, e):
        try:
            _data = self.win_ccl.get()
            _show = _data[1]
            self.win_ui.label_ccl_time['text'] = _data[0]
            self.win_ui.label_ccl_data['text'] = _show
            pyperclip.copy(_data[2])
            self.do_show_info('持仓量 复制成功')
        except Exception as e:
            self.do_show_info('获取失败')
            write_log('{}\n{}'.format(e, format_exc()))

    def thread_win_ui_tick_event(self):
        while True:
            sleep(0.1)
            if self.var_info_ts > 0:
                self.var_info_ts -= 1
                if self.var_info_ts == 0:
                    self.win_ui.lable_info['text'] = ''

    def thread_win_ui_logic_event(self):
        while True:
            sleep(0.1)


if __name__ == '__main__':
    app = App()