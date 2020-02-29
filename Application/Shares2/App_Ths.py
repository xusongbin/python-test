#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyperclip
from tkinter import *

from my_driver import *
from history_parse import ParseFile
from north_fetch import North


class Layout(object):
    def __init__(self, win):
        assert isinstance(win, Tk)
        self.win = win
        self.win.title('test')
        self.win.geometry('500x300')

        self.label_time = Label(self.win, text='数据时间', anchor="w")
        self.label_time.place(x=120, y=20, width=130, height=20)
        self.lable_data = Label(self.win, text='数据内容', anchor="w")
        self.lable_data.place(x=270, y=20, width=150, height=20)
        self.lable_info = Label(self.win, text='', anchor="w")
        self.lable_info.place(x=0, y=220, width=300, height=20)

        self.label_1A0001_name = Label(self.win, text='上证指数', anchor="e")
        self.label_1A0001_name.place(x=0, y=60, width=100, height=20)
        self.label_1A0001_time = Label(self.win, text='2020-02-28 16:52:00', anchor="w")
        self.label_1A0001_time.place(x=120, y=60, width=130, height=20)
        self.label_1A0001_data = Label(self.win, text='3000.00', anchor="w")
        self.label_1A0001_data.place(x=270, y=60, width=150, height=20)

        self.label_881155_name = Label(self.win, text='银行指数', anchor="e")
        self.label_881155_name.place(x=0, y=100, width=100, height=20)
        self.label_881155_time = Label(self.win, text='2020-02-28 16:53:00', anchor="w")
        self.label_881155_time.place(x=120, y=100, width=130, height=20)
        self.label_881155_data = Label(self.win, text='3100.00', anchor="w")
        self.label_881155_data.place(x=270, y=100, width=150, height=20)

        self.label_NORTH_name = Label(self.win, text='北向资金', anchor="e")
        self.label_NORTH_name.place(x=0, y=140, width=100, height=20)
        self.label_NORTH_time = Label(self.win, text='2020-02-28 16:54:00', anchor="w")
        self.label_NORTH_time.place(x=120, y=140, width=130, height=20)
        self.label_NORTH_data = Label(self.win, text='3200.00', anchor="w")
        self.label_NORTH_data.place(x=270, y=140, width=150, height=20)

        self.label_USDCNH_name = Label(self.win, text='离岸人民币', anchor="e")
        self.label_USDCNH_name.place(x=0, y=180, width=100, height=20)
        self.label_USDCNH_time = Label(self.win, text='2020-02-28 16:55:00', anchor="w")
        self.label_USDCNH_time.place(x=120, y=180, width=130, height=20)
        self.label_USDCNH_data = Label(self.win, text='3300.00', anchor="w")
        self.label_USDCNH_data.place(x=270, y=180, width=150, height=20)


class App(object):
    def __init__(self):
        self.win = Tk()
        self.win_ui = Layout(self.win)
        self.win_parse = ParseFile()
        self.win_north = North()

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
        self.win_ui.label_881155_data.bind('<Button-1>', self.on_label_881155_data_click)
        self.win_ui.label_USDCNH_data.bind('<Button-1>', self.on_label_usdcnh_data_click)
        self.win_ui.label_NORTH_data.bind('<Button-1>', self.on_label_north_data_click)

    def do_show_info(self, msg):
        write_log(msg)
        self.win_ui.lable_info['text'] = msg
        self.var_info_ts = 15

    def on_label_1a0001_data_click(self, e):
        try:
            _data = self.win_parse.parse_1a0001(1)[0]
            self.win_ui.label_1A0001_time['text'] = _data[0]
            self.win_ui.label_1A0001_data['text'] = _data[-1]
            pyperclip.copy(_data[-1])
            self.do_show_info('上证指数 复制成功 {}'.format(_data[-1]))
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_881155_data_click(self, e):
        try:
            _data = self.win_parse.parse_881155(1)[0]
            self.win_ui.label_881155_time['text'] = _data[0]
            self.win_ui.label_881155_data['text'] = _data[-1]
            pyperclip.copy(_data[-1])
            self.do_show_info('银行指数 复制成功 {}'.format(_data[-1]))
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_usdcnh_data_click(self, e):
        try:
            _data = self.win_parse.parse_usdcnh(1)[0]
            self.win_ui.label_USDCNH_time['text'] = _data[0]
            self.win_ui.label_USDCNH_data['text'] = _data[-1]
            pyperclip.copy(_data[-1])
            self.do_show_info('离岸人民币 复制成功 {}'.format(_data[-1]))
        except Exception as e:
            write_log('{}\n{}'.format(e, format_exc()))

    def on_label_north_data_click(self, e):
        try:
            _data = self.win_north.fetch()[-1]
            _text = '{}\t{}\t{}'.format(_data[1], _data[2], _data[3])
            self.win_ui.label_NORTH_time['text'] = _data[0]
            self.win_ui.label_NORTH_data['text'] = _text
            pyperclip.copy(_text)
            self.do_show_info('北向资金 复制成功 {}'.format(_text))
        except Exception as e:
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
