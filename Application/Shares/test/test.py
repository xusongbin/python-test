
import os
import re
import gzip
import threading
import urllib.request as ur
import http.cookiejar
import chardet
import json
import sqlite3
import xlwings as xw
import requests
import psutil
from selenium import webdriver
from wxpy import *

import itchat
from apscheduler.schedulers.background import BlockingScheduler

from time import time, sleep, strftime, strptime, localtime, mktime

database_log_table = 'DATA_TABLE'
database_log_item = 'TIME,TOTAL'
database_log_form = '(TIME DATETIME PRIMARY KEY,TOTAL INTEGER);'


def write_log(_data):
    _data = strftime("%Y-%m-%d %H:%M:%S ", localtime()) + _data
    try:
        print(_data)
        with open('log.txt', 'a+') as f:
            f.write(_data + '\n')
    except Exception as e:
        print('write log exception %s' % e)


class SQLite3(object):
    def __init__(self, db=''):
        self.db = db
        self.conn = sqlite3.connect(self.db, check_same_thread=False)

    def set_database(self, db):
        if self.db != db:
            self.db = db
            self.conn.close()
            self.conn = sqlite3.connect(self.db)

    def set_close(self):
        self.conn.close()

    def get_table(self, name):
        try:
            data = self.conn.cursor().execute(
                'select COUNT(*) from sqlite_master where type=\'table\' and name=\'%s\'' % name).fetchall()
            if data[0][0] == 1:
                return True
            return False
        except Exception as e:
            write_log('search table failure %s' % e)
            return False

    def set_create(self, name, desc, data):
        try:
            self.conn.cursor().execute('CREATE %s %s %s' % (name, desc, data))
            return True
        except Exception as e:
            write_log('create %s exception %s' % (name, e))
            return False

    def set_drop(self, name, desc):
        try:
            self.conn.cursor().execute('DROP %s %s' % (name, desc))
            return True
        except Exception as e:
            write_log('drop %s:%s exception %s' % (name, desc, e))
            return False

    def set_insert(self, table, desc, data):
        try:
            self.conn.cursor().execute('insert into %s(%s) values(%s)' % (table, desc, data))
            return True
        except Exception as e:
            write_log('insert exception %s' % e)
            return False

    def set_update(self, table, desc, data, condition=''):
        try:
            if condition == '':
                self.conn.cursor().execute('UPDATE %s set (%s) = (%s)' % (table, desc, data))
            else:
                self.conn.cursor().execute('UPDATE %s set (%s) = (%s) where %s' % (table, desc, data, condition))
            return True
        except Exception as e:
            write_log('update exception %s' % e)
            write_log('update exception %s' % desc)
            write_log('update exception %s' % data)
            return False

    def set_replace(self, table, desc, data):
        try:
            self.conn.cursor().execute('replace into %s(%s) values(%s)' % (table, desc, data))
            return True
        except Exception as e:
            write_log('replace exception %s' % e)
            return False

    def set_delete(self, table, desc, data):
        try:
            self.conn.cursor().execute('delete from %s where %s=%s' % (table, desc, data))
            self.conn.commit()
            return True
        except Exception as e:
            write_log('delete exception %s' % e)
            return False

    def get_select(self, table, desc, condition=''):
        try:
            if condition == '':
                data = self.conn.cursor().execute('select %s from %s' % (desc, table)).fetchall()
            else:
                data = self.conn.cursor().execute('select %s from %s WHERE %s' % (desc, table, condition)).fetchall()
            return data
        except Exception as e:
            write_log('select exception %s' % e)
            return False

    def get_condition(self, desc):
        try:
            data = self.conn.cursor().execute(desc).fetchall()
            return data
        except Exception as e:
            write_log('condition exception %s' % e)
            return False

    def set_commit(self):
        try:
            self.conn.commit()
            return True
        except Exception as e:
            write_log('commit exception %s' % e)
            return False


class SharesData(object):
    def __init__(self):
        self.db = SQLite3()
        self.today = strftime("%Y-%m-%d", localtime())
        self.create_table()
        self.data_list = []
        self.data_last = 0
        self.time_last = '2019-03-20 00:00:00'

        self.work_event()

    def create_table(self):
        self.db = SQLite3(self.today + '.db')
        if not self.db.get_table(database_log_table):
            self.db.set_create(
                'TABLE',
                database_log_table,
                database_log_form
            )

    def sjs_get_data(self):
        _id = 'b0a0db1af56d14d87eb435419efbb0f8'
        _url = 'https://api.shenjian.io/?appid=' + _id
        _code = 'sh000001'
        _field = ['date', 'time', 'volume']
        _list = []
        while True:
            try:
                req = ur.Request(_url, headers={'Accept-Encoding': 'gzip'})
                resp = ur.urlopen(req)
                file = gzip.GzipFile(fileobj=resp)
                _str = file.read().decode('UTF-8')
                _js = json.loads(_str)['data']
                for d in _js:
                    if _code == d['code']:
                        for i in _field:
                            _list.append(d[i])
            except:
                pass
            if len(_list) == len(_field):
                break
            _list.clear()
            sleep(0.1)
        return _list

    def parse_list(self, _list):
        if self.data_list[2] != _list[2]:
            self.data_list = _list
            _str = '\'%s %s\', %s' % (self.data_list[0], self.data_list[1], self.data_list[2])
            # write_log(_str)
            self.db.set_insert(
                database_log_table,
                database_log_item,
                _str
            )
            self.db.set_commit()
        _report = False
        _this_time = _list[0] + ' ' + _list[1]
        _this_data = int(_list[2])
        _this_time_stamp = int(mktime(strptime(_this_time, "%Y-%m-%d %H:%M:%S")))
        _last_time_stamp = int(mktime(strptime(self.time_last, "%Y-%m-%d %H:%M:%S")))
        # print(_this_time, _this_data, self.time_last)
        # print(_this_time_stamp, _last_time_stamp)
        if _this_time_stamp - _last_time_stamp > 300:
            _report = True
        if (_this_time_stamp % 300) < 60 < (_this_time_stamp - _last_time_stamp):
            _report = True
        if _report:
            _thid_diff = _this_data - self.data_last
            self.data_last = _this_data
            self.time_last = _this_time
            _str = _this_time + ' = ' + str(_thid_diff)
            write_log(_str)

    def work_event(self):
        while True:
            if strftime("%Y-%m-%d", localtime()) != self.today:
                self.today = strftime("%Y-%m-%d", localtime())
                self.create_table()
            _hour = int(time()) / 60 / 60 % 24
            if _hour < 9 or 12 < _hour < 13 or _hour > 17:
                sleep(60)
                continue
            _list = self.sjs_get_data()
            self.parse_list(_list)
            sleep(5)


def sina_get_data():
    _url = 'http://hq.sinajs.cn/list=sh000001'
    _list = []
    while True:
        try:
            _resp = ur.urlopen(_url).read()
            _resp = _resp.decode(chardet.detect(_resp)['encoding'])
            _para = str(_resp).split(',')
            if len(_para) == 33:
                _list.append(_para[30])
                _list.append(_para[31])
                _list.append(_para[8])
                break
        except:
            pass
        _list.clear()
        sleep(0.1)
    return _list


def dfcf_get_all():
    _url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000011&type=m5k&_=%d' % int(time()*1000)
    _list = []
    while True:
        try:
            _resp = ur.urlopen(_url).read()
            _resp = _resp.decode(chardet.detect(_resp)['encoding'])[1:-1]
            _list = str(_resp).split('\r\n')
            break
        except:
            pass
        _list.clear()
        sleep(0.1)
    return _list


def ths_get_szzs000001():
    # _url_main = 'http://stockpage.10jqka.com.cn/1A0001/'
    # _url_main = 'http://stockpage.10jqka.com.cn/'
    _url_main = 'http://www.10jqka.com'
    _url = 'http://d.10jqka.com.cn/v6/time/16_1A0001/last.js'
    referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'
    url_agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3641.400 QQBrowser/10.4.3284.400')
    _req = ur.Request(_url)
    _req.add_header('User-Agent', url_agent)
    _req.add_header('Referer', referer)
    _req.add_header('Host', 'd.10jqka.com.cn')
    _req.add_header('Cookie', 'v=AifGbxXWN618RLMh1gL5Age6tlDxrPuOVYB_AvmUQ7bd6EmKAXyL3mVQD1cK')
    _resp = ur.urlopen(_req).read()

    _resp = _resp.decode(chardet.detect(_resp)['encoding'])
    # print(_resp)
    if 'quotebridge_v6_time_16_1A0001_last' in _resp:
        _resp = str(_resp).split('(')[1].split(')')[0]
        # print(_resp)
        _resp = json.loads(_resp)['16_1A0001']
        print(_resp['date'])
        for d in _resp['data'].split(';'):
            print(d)
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    else:
        print('cookie invalid!')

    # cookie = http.cookiejar.CookieJar()
    # handler = ur.HTTPCookieProcessor(cookie)
    # opener = ur.build_opener(handler)
    # _resp = opener.open(_url_main)
    # print(cookie)
    #
    # for i in cookie:
    #     print('%s = %s' % (i.name, i.value))


def ths_get_yh881155():
    _url = 'http://d.10jqka.com.cn/v2/time/48_881155/last.js'
    referer = 'http://t.10jqka.com.cn/guba/881155/'
    url_agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3641.400 QQBrowser/10.4.3284.400')
    _req = ur.Request(_url)
    _req.add_header('User-Agent', url_agent)
    _req.add_header('Referer', referer)
    # _req.add_header('Host', 'd.10jqka.com.cn')
    # _req.add_header('Cookie', 'v=AifGbxXWN618RLMh1gL5Age6tlDxrPuOVYB_AvmUQ7bd6EmKAXyL3mVQD1cK')
    _resp = ur.urlopen(_req).read()

    _resp = _resp.decode(chardet.detect(_resp)['encoding'])
    # print(_resp)
    if 'quotebridge_v2_time_48_881155_last' in _resp:
        _resp = str(_resp).split('(')[1].split(')')[0]
        # print(_resp)
        _resp = json.loads(_resp)['48_881155']
        print(_resp['date'])
        for d in _resp['data'].split(';'):
            print(d)
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    else:
        print('request invalid!')


def get_cookie():
    # _url = 'http://stockpage.10jqka.com.cn/1A0001/'
    _url = 'http://www.10jqka.com'
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=opt)
    driver.get('http://stockpage.10jqka.com.cn/1A0001/')
    _cookie = ''
    for d in driver.get_cookies():
        if d['name'] == 'v':
            _cookie = 'v=' + d['value']
    driver.delete_all_cookies()
    print(_cookie)


def save_xlsx():
    # data_date = '20190321'
    # data_data = [('0935', 24188375), ('0940', 15407101), ('0945', 12553845), ('0950', 13754642), ('0955', 11976948),
    #              ('1000', 10493080), ('1005', 8794734), ('1010', 9844257), ('1015', 9439424), ('1020', 11527316),
    #              ('1025', 7926978), ('1030', 7302290), ('1035', 6613540), ('1040', 9307340), ('1045', 7668640),
    #              ('1050', 7947550), ('1055', 7777360), ('1100', 7420320), ('1105', 6556220), ('1110', 7084010),
    #              ('1115', 5059790), ('1120', 4984450), ('1125', 5763100), ('1130', 6533330), ('1305', 17269100),
    #              ('1310', 8202220), ('1315', 7435350), ('1320', 6936440), ('1325', 6194220), ('1330', 7040360),
    #              ('1335', 7803480), ('1340', 9364380), ('1345', 7709030), ('1350', 5612490), ('1355', 5629300),
    #              ('1400', 9831890), ('1405', 8025370), ('1410', 5394520), ('1415', 5031140), ('1420', 6260090),
    #              ('1425', 5589000), ('1430', 5959990), ('1435', 6678910), ('1440', 7296240), ('1445', 8163100),
    #              ('1450', 11183860), ('1455', 13221190), ('1500', 11892570)]
    data_date = '20190322'
    data_data = [('0935', 24188375), ('0940', 15407101), ('0945', 12553845), ('0950', 13754642), ('0955', 11976948),
                 ('1000', 10493080), ('1005', 8794734), ('1010', 9844257), ('1015', 9439424), ('1020', 11527316),
                 ('1025', 7926978), ('1030', 7302290), ('1035', 6613540), ('1040', 9307340), ('1045', 7668640),
                 ('1050', 7947550), ('1055', 7777360), ('1100', 7420320), ('1105', 6556220), ('1110', 7084010),
                 ('1115', 5059790), ('1120', 4984450), ('1125', 5763100), ('1130', 6533330), ('1305', 17269100),
                 ('1310', 8202220), ('1315', 7435350), ('1320', 6936440), ('1325', 6194220), ('1330', 7040360),
                 ('1335', 7803480), ('1340', 9364380), ('1345', 7709030), ('1350', 5612490), ('1355', 5629300),
                 ('1400', 9831890), ('1405', 8025370), ('1410', 5394520), ('1415', 5031140), ('1420', 6260090),
                 ('1425', 5589000), ('1430', 5959990), ('1435', 6678910), ('1440', 7296240), ('1445', 8163100),
                 ('1450', 11183860), ('1455', 13221190), ('1500', 11892570)]
    xlsx_x = ('9:35,9:40,9:45,9:50,9:55,'
              '10:00,10:05,10:10,10:15,10:20,10:25,10:30,10:35,10:40,10:45,10:50,10:55,'
              '11:00,11:05,11:10,11:15,11:20,11:25,11:30,'
              '13:05,13:10,13:15,13:20,13:25,13:30,13:35,13:40,13:45,13:50,13:55,'
              '14:00,14:05,14:10,14:15,14:20,14:25,14:30,14:35,14:40,14:45,14:50,14:55,15:00,')

    data_date = data_date[0:4] + '-' + data_date[4:6] + '-' + data_date[6:] + ' 00:00:00'
    path = os.getcwd() + '\上证.xlsx'
    # wb = xw.App(visible=False, add_book=False).books.open(path)
    wb = xw.Book(path)
    save_flag = False
    try:
        # 获取表格
        sht = wb.sheets['上证指数5分钟']
        # 判断第一列时间参数是否正确，否则重新写入
        for i in range(2, 50):
            rng = sht.range('A' + str(i))
            if rng.value != xlsx_x.split(',')[i-2]:
                rng.value = xlsx_x.split(',')[i - 2]
                save_flag = True
        # 判断第一行是否存在当前参数，否则新增一列，第一行写入当前日期
        col_max = sht.range('A1').expand('table').columns.count
        if col_max == 1:
            col_max += 1
        cur = 0
        for i in range(2, col_max + 1):
            rng = sht.range((1, i))
            if rng.value is None:
                cur = i
                print('cell none ', cur)
                rng = sht.range((1, cur))
                rng.value = data_date
                rng.columns.autofit()
                # rng.column_width = 11
                save_flag = True
            else:
                _date = str(rng.value)
                if _date == data_date:
                    cur = i
                    print('date exist ', cur)
                else:
                    print('date diff ({}!={})'.format(_date, data_date))
        # 判断当前日期下的数据是否一致，否则更新数据
        for i in range(len(data_data)):
            row = i + 2
            rng = sht.range((row, cur))
            _data = int(data_data[i][1]/10000) + 200
            if rng.value != _data:
                rng.value = _data
                save_flag = True
    except:
        pass
    if save_flag:
        wb.save()
    wb.app.kill()


def wechat():
    thread_data = threading.Thread(target=fun_wechat_kill_proc)
    thread_data.setDaemon(True)
    thread_data.start()

    bot = Bot(cache_path=True, qr_path='login.jpg')

    while True:
        print('search')
        try:
            g = bot.groups()
            if g:
                my_group = bot.groups().search('A小号群2')[0]
                my_group.send_image('test.jpg')
        except:
            pass
        sleep(5)
    bot.join()


def fun_wechat_kill_proc():
    flag = True
    while flag:
        for proc in psutil.process_iter():
            if 'dllhost.exe' in proc.name():
                os.system('taskkill /IM dllhost.exe /F')
                flag = False
        sleep(1)


def fun_wechat_send_group(bot):
    while True:
        try:
            if bot.groups():
                my_group = bot.groups().search('A小号群2')[0]
                print(my_group)
            if bot.friends():
                print(bot.friends())
        except:
            pass
        sleep(1)


def myitchat():
    itchat.auto_login(hotReload=True, picDir='login.jpg')
    rooms = itchat.get_chatrooms(update=True)
    username = ''
    for room in rooms:
        if room['NickName'] == 'A小号群2':
            username = room['UserName']
            break
    print(username)
    if username != '':
        try:
            # _f = os.getcwd() + '\\tmp.jpg'
            itchat.send_image('tmp.jpg', toUserName=username)
            itchat.send_msg('test', toUserName=username)
        except Exception as e:
            print('itchat except: %s' % e)


def test_xlsx_chart():
    path = os.getcwd() + '\\test.xlsx'
    wb = xw.Book(path)
    try:
        ws = wb.sheets['上证指数5分钟']
        chart = ws.charts['图表 1']
        chart.api[1].ChartTitle.Text = '111'
    except:
        pass
    wb.app.quit()


if __name__ == '__main__':
    # sd = SharesData()
    # ths_get_szzs000001()
    # ths_get_yh881155()
    # save_xlsx()
    # get_cookie()
    # wechat()
    # myitchat()
    test_xlsx_chart()
