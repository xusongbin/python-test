#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import poplib
from time import time, mktime, strptime, strftime, localtime, sleep
from email.parser import BytesParser
from email.policy import default
from traceback import format_exc

'''
1、调试邮件收集掉线信息
2、调试重启软件接口
'''


class DDAssist(object):
    # application path
    path_dd = r'C:\Users\Administrator\Desktop\ddProxy\ddProxy.exe'
    name_dd = os.path.basename(path_dd)
    name_ss = 'scavenger-skywalker.exe'

    # smtp infomation
    pop_server = 'pop.163.com'
    pop_usr = 'ak3336105@163.com'
    pop_pwd = '52023921033'
    usr_name = pop_usr.split('@')[0]

    # local msg
    local_file = 'email.info'

    def __init__(self):
        try:
            self.ec = poplib.POP3(self.pop_server)
            self.ec.user(self.pop_usr)
            self.ec.pass_(self.pop_pwd)
            self.run()
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))

    def ss_close(self):
        resp = os.popen('taskkill /f /t /im {}'.format(self.name_ss)).read().strip()
        if resp:
            print(resp)

    def dd_open(self):
        os.system('start {}'.format(self.path_dd))

    def dd_close(self):
        resp = os.popen('taskkill /f /t /im {}'.format(self.name_dd)).read().strip()
        if resp:
            print(resp)

    def dd_restart(self):
        self.dd_close()
        self.dd_open()

    def dd_find(self):
        resp = os.popen('tasklist|findstr "{}"'.format(self.name_dd)).read().strip()
        if resp:
            return True
        return False

    def read_rows2list(self):
        if not os.path.isfile(self.local_file):
            return []
        with open(self.local_file, 'r', encoding='utf-8') as f:
            return f.read().split('\n')

    def write_rows2file(self, rows):
        with open(self.local_file, 'w', encoding='utf-8') as f:
            for row in rows:
                f.write('{}\n'.format(row))

    def check_tdata(self, ts, data):
        data = '{},{}'.format(ts, data.split('\n')[0].strip())
        if '矿机' not in data:
            return False
        rows = self.read_rows2list()
        row_new = []
        for row in rows:
            if not re.match(r'\d+,.*', row):
                continue
            if '矿机' not in row:
                continue
            ts, msg = row.split(',')
            if (time()-int(ts)) >= 60*60*24*7:
                continue
            row_new.append(row)
        for row in row_new:
            if row == data:
                return False
        row_new.append(data)
        self.write_rows2file(row_new)
        return True

    def email_execute(self, data):
        if '心跳已停止' in data:
            print('检查到心跳已停止：重启dd软件')
            self.dd_restart()
        elif '没有扫出DL了' in data:
            print('检查到DL提交异常：关闭ss软件')
            self.ss_close()

    def email_parse(self, ts, msg):
        for part in msg.walk():
            # 如果maintype是multipart，说明是容器（用于包含正文、附件等）
            if part.get_content_maintype() == 'multipart':
                continue
            # 如果maintype是multipart，说明是邮件正文部分
            elif part.get_content_maintype() == 'text':
                date = strftime("%Y-%m-%d %H:%M:%S", localtime(ts))
                data = str(part.get_content()).split('\n')[0]
                if not self.check_tdata(ts, data):
                    # print('旧邮件{}=>{}'.format(date, data))
                    continue
                print('新邮件{}=>{}'.format(date, data))
                self.email_execute(data)

    def email_recv(self):
        try:
            # 获取服务器上的邮件列表，相当于发送POP 3的list命令
            # resp保存服务器的响应码
            # mails列表保存每封邮件的编号、大小
            resp, mails, octets = self.ec.list()
            # 获取服务器上的邮件列表，相当于发送POP 3的list命令
            if len(mails) <= 0:
                return False
            start = max(len(mails)-20, 1)
            for i in range(start, len(mails) + 1):
                resp, data, octets = self.ec.retr(i)
                msg_data = b'\r\n'.join(data)
                # 将字符串内容解析成邮件，此处一定要指定policy=default
                msg = BytesParser(policy=default).parsebytes(msg_data)
                # print('发件人:' + msg['from'])
                # print('收件人:' + msg['to'])
                # print('主题:' + msg['subject'])
                # print('第一个收件人名字:' + msg['to'].addresses[0].username)
                # print('第一个发件人名字:' + msg['from'].addresses[0].username)
                if msg['from'].addresses[0].username != self.usr_name:
                    # 删除非本人发送的邮件
                    self.ec.dele(i)
                    continue
                if '矿机' not in msg['subject']:
                    # 删除非矿机邮件
                    self.ec.dele(i)
                    continue
                date, zoom = str(msg['date']).split('+')
                ts = int(mktime(strptime(date.strip(), '%a, %d %b %Y %H:%M:%S')))
                cts = time()
                if (cts - ts) >= 60 * 60 * 24 * 7:
                    # 删除超过一周的邮件
                    # self.ec.dele(i)
                    continue
                if (cts - ts) >= 60 * 60 * 24 * 1:
                    # 忽略超过一天的邮件
                    continue
                self.email_parse(ts, msg)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
            self.ec = poplib.POP3(self.pop_server)
            self.ec.user(self.pop_usr)
            self.ec.pass_(self.pop_pwd)
        return True

    def run(self):
        print('启动DD辅助监控软件 {}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
        while True:
            if not self.dd_find():
                print('检查到dd软件未启动：打开dd软件')
                self.dd_open()
            self.email_recv()
            sleep(30)


if __name__ == '__main__':
    dda = DDAssist()
