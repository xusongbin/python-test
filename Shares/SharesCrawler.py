
import os
import sys
import shutil
import queue
import threading
import chardet
import json
import xlwings as xw
from PIL import Image

from wxpy import *

from selenium import webdriver
from time import sleep, localtime, strftime, time

import urllib.request

from win32com.client import Dispatch
import pythoncom

from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import QCoreApplication, Qt, QTimer
from PyQt5.QtGui import QPixmap

import ui_shares


def write_log(_data):
    _data = strftime("%Y-%m-%d %H:%M:%S ", localtime()) + _data
    try:
        print(_data)
        with open('log.txt', 'a+') as f:
            f.write(_data + '\n')
    except Exception as e:
        print('write log exception %s' % e)


# 启用win32模块导出excel的图表，图表需要打开加载缓存才能导出
class Pyxlchart(object):
    # This class exports charts in an Excel Spreadsheet to the FileSystem
    # win32com libraries are required.
    def __init__(self):
        # 初始化图表
        pythoncom.CoInitialize()
        self.WorkbookDirectory = ''     # excel文件所在目录
        self.WorkbookFilename = ''      # 文件名称
        self.GetAllWorkbooks = False    # 获取所有book
        self.SheetName = ''         # sheet名称
        self.ChartName = ''         # 导出单张图表时，指定图表名称
        self.GetAllWorkbookCharts = False
        self.GetAllWorksheetCharts = True
        self.ExportPath = ''        # 导出的文件路径
        self.ImageFilename = ''     # 导出的图片名称
        self.ReplaceWhiteSpaceChar = '_'
        self.ImageType = 'jpg'

    def __del__(self):
        pass

    def start_export(self, _visible=False):
        if self.WorkbookDirectory == '':
            return "WorkbookDirectory not set"
        else:
            self._export(_visible)

    def _export(self, _visible):
        # Exports Charts as determined by the settings in class variabels.
        excel = Dispatch("excel.application")
        # 启用独立的进程调用excel，Dispatch容易冲突【会强行关闭正在打开的excel】
        # 使用 DispatchEx为单独调用线程，不影响已经打开的excel

        excel.Visible = _visible
        wb = excel.Workbooks.Open(os.path.join(self.WorkbookDirectory, self.WorkbookFilename))

        if self.SheetName != "" and self.ChartName != "":
            while True:
                sleep(0.5)
                sht = self._change_sheet(wb, self.SheetName)
                cht = sht.ChartObjects(self.ChartName)
                if cht:
                    break
        '''
        time.sleep(3)  # 等5秒等待进程打开加载文档
        # 使用打开excel的方式，则模拟键盘事件触发加载所有图表
        if excel.Visible == 1 or excel.Visible is True:
            win32api.keybd_event(17, 0, 0, 0)  # 键盘按下  ctrl键
            time.sleep(1)
            for k in range(4):
                win32api.keybd_event(34, 0, 0, 0)  # ctrl+pageDown的组合会跳转sheet，20次跳转可以到最后的图表
            win32api.keybd_event(36, 0, 0, 0)  # 键盘按下  home键，和上个按键形成组合键，回到第一行开头
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(36, 0, win32con.KEYEVENTF_KEYUP, 0)

            # 当表格过大时，只能保存到页面显示的图标，故此需要先循环翻页将所有图片加载
            for i in range(15):  # 翻页加载所有图表
                win32api.keybd_event(34, 0, 0, 0)  # 每次读取之后翻页
                win32api.keybd_event(34, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.5)
        '''

        # 图片加载完成，好了，导出图片继续进行
        self._get_Charts_In_Worksheet(wb, self.SheetName, self.ChartName)
        wb.Close(True)
        excel.Quit()

    def _get_Charts_In_Worksheet(self, wb, worksheet="", chartname=""):
        if worksheet != "" and chartname != "":
            sht = self._change_sheet(wb, worksheet)
            cht = sht.ChartObjects(chartname)

            self._save_chart(cht)
            return
        if worksheet == "":  # 导出表格中所有图表
            for sht in wb.Worksheets:
                for cht in sht.ChartObjects():
                    if chartname == "":
                        self._save_chart(cht)
                    else:
                        if chartname == cht.Name:
                            self._save_chart(cht)
        else:   # 导出指定sheet中的图标
            sht = wb.Worksheets(worksheet)
            for cht in sht.ChartObjects():
                if chartname == "":
                    self._save_chart(cht)
                else:
                    if chartname == cht.Name:
                        self._save_chart(cht)

    def _change_sheet(self, wb, worksheet):
        try:
            return wb.Worksheets(worksheet)
        except:
            raise NameError('Unable to Select Sheet: ' + worksheet + ' in Workbook: ' + wb.Name)

    def _save_chart(self, chartobject):
        # 保存图标到指定路径
        # :param chartObject: 图表名称
        # :return:
        imagename = self._get_filename(chartobject.Name)
        savepath = os.path.join(self.ExportPath, imagename)
        # write_log(savepath)

        chartobject.Chart.Export(savepath, self.ImageType)

    def _get_filename(self, chartname):
        # 获取导出图表的文件名称
        # Replaces white space in self.WorkbookFileName with the value given in self.ReplaceWhiteSpaceChar
        # If self.ReplaceWhiteSpaceChar is an empty string then self.WorkBookFileName is left as is
        if self.ReplaceWhiteSpaceChar != '':
            chartname.replace(' ', self.ReplaceWhiteSpaceChar)
        if self.ImageFilename == '':    # 未指定导出的图片名称，则与图表名称一致
            return chartname + "." + self.ImageType
        else:   # 指定了导出图片的命名格式
            return self.ImageFilename + "_" + chartname + "." + self.ImageType


class Shares(object):
    def __init__(self):
        self.tp = 0
        self.cookies_qq = queue.Queue(10)
        self.text_qq = queue.Queue()
        # self.image_qq = queue.Queue()
        self.xlsx_szzs000001_data = []
        self.xlsx_szzs000001_path = os.getcwd() + '\szzs000001.xlsx'
        self.xlsx_szzs000001_sheet = '上证指数5分钟'
        self.xlsx_yh881155_data = []
        self.xlsx_yh881155_path = os.getcwd() + '\yh881155.xlsx'
        self.xlsx_yh881155_sheet = '银行指数5分钟'
        self.wb_szzs = None
        self.thread_data_tick = 0
        self.work_thread = True

        os.system('taskkill /im chrome.exe -f')
        os.system('taskkill /im chromedriver.exe -f')

        self.xlsxchart = Pyxlchart()

        opt = webdriver.ChromeOptions()
        opt.set_headless()
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=opt)

        self.work_widget = QWidget()
        self.work_widget.setAttribute(Qt.WA_QuitOnClose, True)

        self.work_dialog = QDialog()
        self.work_ui = ui_shares.Ui_Form()
        self.work_ui.setupUi(self.work_dialog)
        self.work_dialog.setAttribute(Qt.WA_QuitOnClose, False)
        self.work_dialog.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.work_ui.checkBoxUpdate.setChecked(True)
        self.work_ui.pushButton.setText('停止')
        self.work_ui.pushButton.clicked.connect(self.fun_btn_clicked)

        self.bot = Bot(cache_path=True, qr_path='login.jpg')
        # self.bot.join()

        self.thread_cookies = threading.Thread(target=self.thread_cookies_event)
        self.thread_cookies.setDaemon(True)
        self.thread_cookies.start()

        self.thread_data = threading.Thread(target=self.fun_get_data)
        self.thread_data.setDaemon(True)
        self.thread_data.start()

        self.timer_work_ui = QTimer()
        self.timer_work_ui.timeout.connect(self.timer_work_ui_event)
        self.timer_work_ui.start(10)

    def show(self):
        self.work_dialog.show()
        self.text_qq.put('启动')

    def fun_btn_clicked(self):
        if self.work_ui.pushButton.text() == '启动':
            self.work_ui.pushButton.setText('停止')
        else:
            self.work_ui.pushButton.setText('启动')

    def thread_cookies_event(self):
        _cookie_sta = 0
        while self.work_thread:
            if self.cookies_qq.full():
                _cookie_sta = 10
                # write_log('cookie full!')
                sleep(3)
                continue
            _cookie = ''
            try:
                self.driver.get('http://stockpage.10jqka.com.cn/1A0001/')
                for d in self.driver.get_cookies():
                    if d['name'] == 'v':
                        _cookie = 'v=' + d['value']
                self.driver.delete_all_cookies()
            except Exception as e:
                write_log('get cookie except: %s' % e)
            if _cookie != '':
                self.cookies_qq.put(_cookie)
                self.cookies_qq.put(_cookie)
                _cookie_sta += 1
                if _cookie_sta == 1:
                    self.text_qq.put('获取cookie正常')
                write_log('cookie put: %s' % _cookie)
            else:
                # write_log('cookie none!')
                pass
        self.driver.quit()

    def fun_get_data(self):
        self.thread_data_tick = 5
        while self.work_thread:
            sleep(1)
            if not self.cookies_qq.empty():
                if self.work_ui.pushButton.text() == '启动':
                    continue
                self.thread_data_tick -= 1
                if self.thread_data_tick > 0:
                    continue
                self.thread_data_tick = 5

                self.fun_fetch_szzs000001()
                self.fun_fetch_yh881155()
            else:
                self.thread_data_tick = 5
                write_log('cookie empty!')
        try:
            self.wb_szzs.app.kill()
        except Exception as e:
            write_log('close wb except: %s' % e)

    def fun_parse_data_to_5m(self, data):
        self.tp = 0
        _list = []
        ll = str(data).split(';')
        for i, d in enumerate(ll):
            p = str(d).split(',')
            if int(p[0]) % 5 == 0:
                _time = p[0]
                _volumn = 0
                if int(p[0]) == 930 or int(p[0]) == 1300:
                    continue
                else:
                    if int(p[0]) == 935 or int(p[0]) == 1305:
                        p = str(ll[i - 5]).split(',')
                        _volumn += int(p[4])
                    p = str(ll[i]).split(',')
                    _volumn += int(p[4])
                    p = str(ll[i-1]).split(',')
                    _volumn += int(p[4])
                    p = str(ll[i-2]).split(',')
                    _volumn += int(p[4])
                    p = str(ll[i-3]).split(',')
                    _volumn += int(p[4])
                    p = str(ll[i-4]).split(',')
                    _volumn += int(p[4])
                _volumn = int(_volumn/100)
                _list.append((_time, _volumn))
        return _list

    def fun_fetch_szzs000001(self):
        szzs_url = 'http://d.10jqka.com.cn/v6/time/16_1A0001/last.js'
        host = 'd.10jqka.com.cn'
        referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'
        url_agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3641.400 QQBrowser/10.4.3284.400')

        _cookie = self.cookies_qq.get()
        _req = urllib.request.Request(szzs_url)
        _req.add_header('User-Agent', url_agent)
        _req.add_header('Referer', referer)
        _req.add_header('Host', host)
        _req.add_header('Cookie', _cookie)
        _resp = urllib.request.urlopen(_req).read()
        _resp = _resp.decode(chardet.detect(_resp)['encoding'])

        if 'quotebridge_v6_time_16_1A0001_last' in _resp:
            _resp = str(_resp).split('(')[1].split(')')[0]
            _resp = json.loads(_resp)['16_1A0001']
            # write_log(_resp['date'])
            # write_log(_resp['data'])
            _date = _resp['date']
            _data = self.fun_parse_data_to_5m(_resp['data'])
            if len(self.xlsx_szzs000001_data) < len(_data):
                print(_resp['data'])
                if self.fun_save_data_to_xlsx(
                    self.xlsx_szzs000001_path,
                    self.xlsx_szzs000001_sheet,
                    '上证指数',
                        _date,
                        _data,
                        _resp['data']):
                    self.xlsx_szzs000001_data = _data
                    write_log('save xlsx_szzs000001 pass!')
                else:
                    write_log('save xlsx_szzs000001 fail!')
            # write_log(strftime("%Y-%m-%d %H:%M:%S", localtime()))

    def fun_fetch_yh881155(self):
        szzs_url = 'http://d.10jqka.com.cn/v2/time/48_881155/last.js'
        referer = 'http://t.10jqka.com.cn/guba/881155/'
        url_agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3641.400 QQBrowser/10.4.3284.400')

        _req = urllib.request.Request(szzs_url)
        _req.add_header('User-Agent', url_agent)
        _req.add_header('Referer', referer)
        _resp = urllib.request.urlopen(_req).read()
        _resp = _resp.decode(chardet.detect(_resp)['encoding'])

        if 'quotebridge_v2_time_48_881155_last' in _resp:
            _resp = str(_resp).split('(')[1].split(')')[0]
            _resp = json.loads(_resp)['48_881155']
            # write_log(_resp['date'])
            # write_log(_resp['data'])
            _date = _resp['date']
            _data = self.fun_parse_data_to_5m(_resp['data'])
            if len(self.xlsx_yh881155_data) < len(_data):
                print(_resp['data'])
                if self.fun_save_data_to_xlsx(
                    self.xlsx_yh881155_path,
                    self.xlsx_yh881155_sheet,
                    '银行指数',
                        _date,
                        _data,
                        _resp['data']):
                    self.xlsx_yh881155_data = _data
                    write_log('save xlsx_yh881155_path pass!')
                else:
                    write_log('save xlsx_yh881155_path fail!')
            # write_log(strftime("%Y-%m-%d %H:%M:%S", localtime()))

    def fun_save_data_to_xlsx(self, path, sheet, name, data_date, data_data, data_json):
        _rt_flag = False
        if not self.work_ui.checkBoxUpdate.isChecked():
            return _rt_flag
        _rt_flag = True
        # write_log(data_data)
        write_log(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        xlsx_x = ('9:35:00,9:40:00,9:45:00,9:50:00,9:55:00,'
                  '10:00:00,10:05:00,10:10:00,10:15:00,10:20:00,'
                  '10:25:00,10:30:00,10:35:00,10:40:00,10:45:00,'
                  '10:50:00,10:55:00,11:00:00,11:05:00,11:10:00,'
                  '11:15:00,11:20:00,11:25:00,11:30:00,13:05:00,'
                  '13:10:00,13:15:00,13:20:00,13:25:00,13:30:00,'
                  '13:35:00,13:40:00,13:45:00,13:50:00,13:55:00,'
                  '14:00:00,14:05:00,14:10:00,14:15:00,14:20:00,'
                  '14:25:00,14:30:00,14:35:00,14:40:00,14:45:00,14:50:00,14:55:00,15:00:00')

        image_date = data_date[0:4] + '-' + data_date[4:6] + '-' + data_date[6:]
        image_time = ''
        data_date = data_date[0:4] + '-' + data_date[4:6] + '-' + data_date[6:] + ' 00:00:00'
        save_flag = False

        self.wb_szzs = xw.Book(path)
        # self.wb_szzs = xw.App(visible=False, add_book=False).books.open(self.xlsx_path)
        # 获取表格
        ws_szzs = self.wb_szzs.sheets[sheet]
        try:
            # 判断第一列时间参数是否正确，否则重新写入
            for i in range(2, 50):
                rng = ws_szzs.range('A' + str(i))
                _value = rng.value
                if _value is not None:
                    _value = int(float(rng.value * 60 * 24) + 0.5)
                    _value = str(int(_value / 60)) + ':' + str(int(_value % 60)).rjust(2, '0') + ':' + '00'
                if _value != xlsx_x.split(',')[i - 2]:
                    rng.value = xlsx_x.split(',')[i - 2]
                    save_flag = True
                    write_log('rewrite time ({} != {})'.format(_value, xlsx_x.split(',')[i - 2]))

            # 判断第一行是否存在当前参数，否则新增一列，第一行写入当前日期
            col_max = ws_szzs.range('A1').expand('table').columns.count
            if col_max == 1:
                col_max += 1
            cur = 0
            for i in range(2, col_max + 2):
                rng = ws_szzs.range((1, i))
                if rng.value is None:
                    cur = i
                    write_log('date new {} {}'.format(data_date, cur))
                    rng = ws_szzs.range((1, cur))
                    rng.value = data_date
                    rng.columns.autofit()
                    # rng.column_width = 11
                    save_flag = True
                    break
                else:
                    _date = str(rng.value)
                    if _date == data_date:
                        cur = i
                        write_log('date exist {} {}'.format(data_date, cur))
                        break
                    else:
                        # write_log('date diff ({}!={})'.format(_date, data_date))
                        pass
            # 判断当前日期下的数据是否一致，否则更新数据
            for i in range(len(data_data)):
                row = i + 2
                rng = ws_szzs.range((row, cur))
                if name == '银行指数':
                    _data = float(data_data[i][1] / 10000)
                else:
                    _data = int(data_data[i][1] / 10000)
                image_time = ''
                _value = 0
                if rng.value is not None:
                    if name == '银行指数':
                        _value = float(rng.value)
                    else:
                        _value = int(rng.value)
                if _value < _data:
                    rng.value = _data
                    save_flag = True
                    image_time = xlsx_x.split(',')[i].replace(':', '')[:-2]
                    write_log('rewrite column:{} row:{} time:{} data:{}'.format(cur, row, xlsx_x.split(',')[i], _data))
                    self.text_qq.put('更新数据 时间：{} 成交量:{}'.format(xlsx_x.split(',')[i], _data))
                elif _value < _data:
                    _rt_flag = False
        except Exception as e:
            write_log('write xlsx except: %s' % e)
            _rt_flag = False
        if save_flag:
            write_log('Save workbook')
            self.wb_szzs.save(path)
            self.text_qq.put('更新表格')
        self.wb_szzs.quit()

        self.xlsxchart.WorkbookDirectory = path[:path.rfind('\\')]
        self.xlsxchart.WorkbookFilename = path[path.rfind('\\')+1:]
        self.xlsxchart.SheetName = sheet
        self.xlsxchart.ExportPath = path[:path.rfind('\\')]
        self.xlsxchart.start_export()

        _image_name = ''
        ifile = ''
        try:
            if image_time != '':
                image_date += ' ' + image_time
            _image_name = '{}-{}.jpg'.format(name, image_date)
            ifile = 'image/' + _image_name
            if not os.path.isdir(ifile[0:ifile.rfind('/') + 1]):
                os.makedirs(ifile[0:ifile.rfind('/') + 1])
            if os.path.exists(ifile):
                os.remove(ifile)
            if os.path.exists('tmp.jpg'):
                os.remove('tmp.jpg')
            if os.path.exists('图表 1.jpg'):
                os.rename('图表 1.jpg', _image_name)
                shutil.copy(_image_name, 'tmp.jpg')
                # img = Image.open(_image_name)
                # img = img.resize((700, 325))
                # img.save(_image_name)
                shutil.move(_image_name, ifile)
                # self.image_qq.put(ifile)
            self.text_qq.put('获取图片：%s' % _image_name)
        except Exception as e:
            write_log('rename image except: %s' % e)
            _rt_flag = False

        try:
            if _image_name != '':
                dfile = 'dat/' + _image_name.split('.')[0] + '.dat'
                if not os.path.isdir(dfile[0:dfile.rfind('/') + 1]):
                    os.makedirs(dfile[0:dfile.rfind('/') + 1])
                with open(dfile, 'w') as f:
                    f.write(data_json)
                    self.text_qq.put('存储日志：%s' % dfile)
        except Exception as e:
            write_log('save dat except: %s' % e)
            _rt_flag = False

        try:
            my_group = self.bot.groups().search('A小号群2')[0]
            if self.work_ui.checkBoxSend.isChecked() and my_group:
                my_group.send_image('tmp.jpg')
                my_group.send(_image_name + ' {}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
                write_log('send wechat tmp.jpg')
                self.text_qq.put('发送图片' + _image_name)
            else:
                write_log('wechat found group err')
        except Exception as e:
            write_log('send wechat except: %s' % e)
            # _rt_flag = False

        return _rt_flag

    def timer_work_ui_event(self):
        if not self.text_qq.empty():
            self.work_ui.plainTextEdit.appendPlainText(self.text_qq.get())

        if self.work_ui.label.text() != str(self.thread_data_tick):
            self.work_ui.label.setText(str(self.thread_data_tick))

        # if not self.image_qq.empty():
        #     im = self.image_qq.get()
        #     self.work_ui.labelImageName.setText(im)
        #     self.work_ui.labelImage.setPixmap(QPixmap(im))

        time = strftime("%Y-%m-%d %H:%M:%S ", localtime())
        if self.work_ui.labelTime.text() != time:
            self.work_ui.labelTime.setText(time)

        if not self.work_dialog.isVisible():
            self.work_thread = False
            sys.exit(0)


def main():
    app = QApplication(sys.argv)
    work = Shares()
    work.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
