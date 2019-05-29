
from time import sleep, strftime, localtime
import os
import win32api
import win32gui
import win32con
import win32clipboard


class TestWindow(object):
    def __init__(self):
        self.flag = False
        self.app_name = '经典彩票计划软件V17.8.exe'
        self.app_path = '经典彩票计划软件V17.8\%s' % self.app_name

        self.wd_name = '经典2017彩票计划分析软件V17.8'
        self.wd_handle = 0
        self.wd_text_handle = 0
        self.wd_dwd_handle = 0
        self.wd_dwd_w_handle = 0
        self.wd_dwd_wdm_handle = 0
        self.wd_dwd_q_handle = 0
        self.wd_dwd_qdm_handle = 0
        self.wd_dwd_b_handle = 0
        self.wd_dwd_bdm_handle = 0
        self.wd_dwd_s_handle = 0
        self.wd_dwd_sdm_handle = 0
        self.wd_dwd_g_handle = 0
        self.wd_dwd_gdm_handle = 0

        # self.app_stop()
        # self.app_run()
        self.get_is_open()
        self.get_wd_text_handle()
        self.get_wd_dwd_handle()

    def app_run(self):
        win32api.ShellExecute(0, 'open', self.app_path, '', '', 0)

    def app_stop(self):
        command = 'taskkill /F /IM %s' % self.app_name
        os.system(command)

    def get_is_open(self):
        if not self.wd_handle:
            self.wd_handle = win32gui.FindWindow(0, self.wd_name)
            self.get_wd_text_handle()
            self.get_wd_dwd_handle()
        return self.wd_handle

    def test_window_handle(self):
        _list = []
        win32gui.EnumWindows(lambda i, param: param.append(i), _list)
        for j in _list:
            if not j:
                continue
            print('窗口句柄：%s' % hex(j).split('x')[1].rjust(8, '0').upper())
            print('窗口标题：%s' % win32gui.GetWindowText(j))
            print('窗口类名：%s' % win32gui.GetClassName(j))
        self.flag = True

    def test_child_handle(self, hd):
        _list = []
        win32gui.EnumChildWindows(hd, lambda i, param: param.append(i), _list)
        for j in _list:
            if not j:
                continue
            print('窗口句柄：%s' % hex(j).split('x')[1].rjust(8, '0').upper())
            print('窗口标题：%s' % win32gui.GetWindowText(j))
            print('窗口类名：%s' % win32gui.GetClassName(j))
        self.flag = True

    def get_wd_text_handle(self):
        _list = []
        win32gui.EnumChildWindows(self.wd_handle, lambda i, param: param.append(i), _list)
        for j in _list:
            if not j:
                continue
            if '计划结果' in win32gui.GetWindowText(j):
                # print('文本框句柄：%s' % hex(j).split('x')[1].rjust(8, '0').upper())
                k = win32gui.FindWindowEx(j, None, None, None)
                # print('文本框句柄：%s' % hex(k).split('x')[1].rjust(8, '0').upper())
                self.wd_text_handle = k

    def get_edit_str(self, hd):
        self.flag = True
        try:
            win32gui.SendMessage(hd, win32con.WM_SETFOCUS)
            win32gui.SendMessage(hd, win32con.EM_SETSEL, 0, -1)
            win32gui.SendMessage(hd, win32con.WM_COPY)
            win32gui.SendMessage(hd, win32con.EM_SETSEL, 0, 0)
            win32clipboard.OpenClipboard()
            _string = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return _string
        except Exception as e:
            print('获取窗口数据异常 %s' % e)
            return ''

    def get_text(self):
        _hd = self.wd_text_handle
        if not _hd:
            print('找不到文本框窗口句柄')
            return ''
        return self.get_edit_str(_hd)

    def get_title_handle(self, hd,  text):
        self.flag = True
        _list = []
        win32gui.EnumChildWindows(hd, lambda i, param: param.append(i), _list)
        for j in _list:
            if not j:
                continue
            if text == win32gui.GetWindowText(j):
                return j
        return 0

    def get_wd_dwd_handle(self):
        _hd = self.get_title_handle(self.wd_handle, '定位胆')
        if not _hd > 0:
            print('获取定位胆窗口句柄失败')
            return
        self.wd_dwd_handle = win32gui.FindWindowEx(_hd, None, None, None)
        self.set_dwd_dm_tab(self.wd_dwd_handle, 0)
        _dwd_w = self.get_title_handle(_hd, '万')
        if not _dwd_w > 0:
            print('获取定位胆万窗口句柄失败')
            return
        self.wd_dwd_w_handle = win32gui.FindWindowEx(_dwd_w, None, None, None)
        self.wd_dwd_wdm_handle = self.get_title_handle(self.wd_dwd_w_handle, '胆码')
        # print('万窗口句柄 %s' % hex(self.dwd_w_handle).split('x')[1].rjust(8, '0').upper())
        self.set_dwd_dm_tab(self.wd_dwd_handle, 1)
        _dwd_q = self.get_title_handle(self.wd_handle, '千')
        if not _dwd_q > 0:
            print('获取定位胆千窗口句柄失败')
            return
        self.wd_dwd_q_handle = win32gui.FindWindowEx(_dwd_q, None, None, None)
        self.wd_dwd_qdm_handle = self.get_title_handle(self.wd_dwd_q_handle, '胆码')
        # print('千窗口句柄 %s' % hex(self.wd_dwd_q_handle).split('x')[1].rjust(8, '0').upper())
        self.set_dwd_dm_tab(self.wd_dwd_handle, 2)
        _dwd_b = self.get_title_handle(self.wd_handle, '百')
        if not _dwd_b > 0:
            print('获取定位胆百窗口句柄失败')
            return
        self.wd_dwd_b_handle = win32gui.FindWindowEx(_dwd_b, None, None, None)
        self.wd_dwd_bdm_handle = self.get_title_handle(self.wd_dwd_b_handle, '胆码')
        # print('百窗口句柄 %s' % hex(self.wd_dwd_b_handle).split('x')[1].rjust(8, '0').upper())
        self.set_dwd_dm_tab(self.wd_dwd_handle, 3)
        _dwd_s = self.get_title_handle(self.wd_handle, '十')
        if not _dwd_s > 0:
            print('获取定位胆十窗口句柄失败')
            return
        self.wd_dwd_s_handle = win32gui.FindWindowEx(_dwd_s, None, None, None)
        self.wd_dwd_sdm_handle = self.get_title_handle(self.wd_dwd_s_handle, '胆码')
        # print('十窗口句柄 %s' % hex(self.wd_dwd_s_handle).split('x')[1].rjust(8, '0').upper())
        self.set_dwd_dm_tab(self.wd_dwd_handle, 4)
        _dwd_g = self.get_title_handle(self.wd_handle, '个')
        if not _dwd_g > 0:
            print('获取定位胆个窗口句柄失败')
            return
        self.wd_dwd_g_handle = win32gui.FindWindowEx(_dwd_g, None, None, None)
        self.wd_dwd_gdm_handle = self.get_title_handle(self.wd_dwd_g_handle, '胆码')
        # print('个窗口句柄 %s' % hex(self.wd_dwd_g_handle).split('x')[1].rjust(8, '0').upper())
        # self.set_dwd_dm_tab(self.wd_dwd_handle, 0)

    def get_dwd_dm_msg(self, hd):
        _list = []
        win32gui.EnumChildWindows(hd, lambda i, param: param.append(i), _list)
        _ms = self.get_edit_str(_list[2])
        _gs = self.get_edit_str(_list[3])
        _qs = self.get_edit_str(_list[6])
        _fb = self.get_edit_str(_list[11])
        return _gs, _qs, _ms, _fb

    def set_dwd_dm_tab(self, hd, num):
        self.flag = True
        win32gui.SendMessage(hd, 0x1300 + 0x30, num, 0)


if __name__ == '__main__':
    test_window = TestWindow()
    if test_window.get_is_open():
        # _data = test_window.get_text()
        # print('获取当前窗口数据 %d' % len(_data))
        _gs, _qs, _ms, _fb = test_window.get_dwd_dm_msg(test_window.wd_dwd_wdm_handle)
        print('定位胆-万-胆码 公式：%s 期数：%s 码数：%s 发布：%s' % (_gs, _qs, _ms, _fb))
    else:
        print('软件未打开')
