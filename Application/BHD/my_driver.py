
import os
import re
import sqlite3
import json
from urllib.request import Request, urlopen
from time import time, sleep
from time import strftime, strptime, localtime, mktime

import shutil


def write_log(_str):
    _data = strftime("%Y-%m-%d %H:%M:%S", localtime())
    _data += '.%03d ' % (int(time() * 1000) % 1000)
    _data += _str
    try:
        print(_data)
        with open('out.log', 'a+') as f:
            f.write(_data + '\n')
    except Exception as e:
        print('write log exception %s' % e)


class MyFile(object):
    def __init__(self, log=True):
        self.log = log

    def mkdir(self, path):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
            return True
        except Exception as e:
            if self.log:
                write_log('File mkdir exception: %s' % e)
        return False

    def create(self, file):
        try:
            if '/' in file:
                if not os.path.isdir(file[0:file.rfind('/') + 1]):
                    os.makedirs(file[0:file.rfind('/') + 1])
            f = open(file, 'w')
            f.close()
        except Exception as e:
            if self.log:
                write_log('File create exception: %s' % e)
            return False
        return True

    def delete(self, file):
        try:
            if os.path.exists(file) is True:
                os.remove(file)
        except Exception as e:
            if self.log:
                write_log('File delete exception: %s' % e)
            return False
        return True

    def copy(self, src, des):
        if self.access(des):
            if not self.delete(des):
                if self.log:
                    write_log('File copy exception: Target file exists.')
                return False
        try:
            shutil.copyfile(src, des)
            return True
        except Exception as e:
            if self.log:
                write_log('File copy exception: %s' % e)
            return False

    def access(self, file):
        try:
            return os.path.exists(file)
        except Exception as e:
            if self.log:
                write_log('File access exception: %s' % e)
            return False

    def get_size(self, file):
        try:
            return os.path.getsize(file)
        except Exception as e:
            if self.log:
                write_log('File get_size exception: %s' % e)
            return -1

    def write(self, file, data, mode='string'):
        # 'string' or 'byte'
        try:
            if not self.access(file):
                return False
            if mode == 'string':
                f = open(file, 'w')
            else:
                f = open(file, 'wb')
            f.write(data)
            f.close()
        except Exception as e:
            if self.log:
                write_log('File write exception: %s' % e)
            return False
        return True

    def append(self, file, data):
        # 'string' or 'byte'
        try:
            if not self.access(file):
                return False
            f = open(file, 'a+')
            f.write(data + '\n')
            f.close()
        except Exception as e:
            if self.log:
                write_log('File append exception: %s' % e)
            return False
        return True

    def read(self, file, mode='string'):
        # 'string' or 'byte'
        try:
            if not self.access(file):
                return False
            if mode == 'string':
                f = open(file, 'r')
            else:
                f = open(file, 'rb')
            _data = f.read()
            f.close()
        except Exception as e:
            if self.log:
                write_log('File read exception: %s' % e)
            return False
        return _data


class MySQLite3(object):
    def __init__(self, db='', log=True):
        self.db = db
        self.log = log
        self.conn = None

    def get_table(self, name):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            data = self.conn.cursor().execute(
                'select COUNT(*) from sqlite_master where type=\'table\' and name=\'{}\''.format(name)).fetchall()
            self.conn.close()
            if data[0][0] == 1:
                return True
            return False
        except Exception as e:
            if self.log:
                write_log('search table failure:%s' % e)
            return False

    def set_create(self, name, desc, data):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.conn.cursor().execute('CREATE %s %s %s' % (name, desc, data))
            self.conn.close()
            return True
        except Exception as e:
            if self.log:
                write_log('create %s exception:%s' % (name, e))
            return False

    def set_drop(self, name, desc):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.conn.cursor().execute('DROP %s %s' % (name, desc))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            if self.log:
                write_log('drop %s:%s exception:%s' % (name, desc, e))
            return False

    def set_insert(self, table, desc, data):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.conn.cursor().execute('insert into %s(%s) values(%s)' % (table, desc, data))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            if self.log:
                write_log('insert exception:%s' % e)
            return False

    def set_update(self, table, desc, data, condition=''):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            if condition == '':
                self.conn.cursor().execute('UPDATE %s set (%s) = (%s)' % (table, desc, data))
            else:
                self.conn.cursor().execute('UPDATE %s set (%s) = (%s) where %s' % (table, desc, data, condition))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            if self.log:
                write_log('update exception:%s' % e)
                write_log('update exception:%s' % desc)
                write_log('update exception:%s' % data)
            return False

    def set_replace(self, table, desc, data):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.conn.cursor().execute('replace into %s(%s) values(%s)' % (table, desc, data))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            if self.log:
                write_log('replace exception:%s' % e)
            return False

    def set_delete(self, table, desc, data):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.conn.cursor().execute('delete from %s where %s=%s' % (table, desc, data))
            self.conn.commit()
            self.conn.close()
            return True
        except Exception as e:
            if self.log:
                write_log('delete exception:%s' % e)
            return False

    def get_select(self, table, desc, condition=''):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            if condition == '':
                data = self.conn.cursor().execute('select %s from %s' % (desc, table)).fetchall()
            else:
                data = self.conn.cursor().execute('select %s from %s WHERE %s' % (desc, table, condition)).fetchall()
            self.conn.close()
            return data
        except Exception as e:
            if self.log:
                write_log('select exception:%s' % e)
            return False


class MyDingTalk(object):
    def __init__(self, web_hook, context_type='MD', log=True):
        self.web_hook = web_hook
        self.context_type = context_type
        self.log = log

    def pack_text(self, data=''):
        _time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        _time += '.%03d ' % (int(time() * 1000) % 1000)
        context = 'Now %s\n' % _time
        for d in data:
            d = d[1].strip()
            if not d:
                continue
            context += '- ' + d + '\n'
        try:
            pack = {'msgtype': 'text', 'text': {'content': context}}
            return json.dumps(pack)
        except Exception as e:
            if self.log:
                write_log('MyDingTalk pack_text except:%s' % str(e))
            return None

    def pack_makedown(self, data=''):
        _time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        _time += '.%03d ' % (int(time() * 1000) % 1000)
        _pack = {'msgtype': 'markdown', 'markdown': ''}
        context = '### Now %s \n' % _time
        if not data:
            return None
        for d in data:
            d = d.strip()
            if not d:
                continue
            context += '- ' + d + '\n'
        _pack['markdown'] = {'title': 'New Message', 'text': context}
        try:
            return json.dumps(_pack)
        except Exception as e:
            if self.log:
                write_log('MyDingTalk pack_makedown except:%s' % str(e))
            return None

    def do_post(self, pkt):
        if not pkt:
            write_log('MyDingTalk post none')
            return False
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        try:
            req = Request(self.web_hook, data=pkt.encode(), headers=headers)
            resp = urlopen(req)
            if json.loads(resp.read())['errcode'] == 0:
                return True
        except Exception as e:
            if self.log:
                write_log('MyDingTalk post except:%s' % str(e))
            return False

    def send(self, data=''):
        if self.context_type == 'MD':
            _pack = self.pack_makedown(data)
        else:
            _pack = self.pack_text(data)
        if self.do_post(_pack):
            if self.log:
                write_log('MyDingTalk send done')
            return True
        else:
            if self.log:
                write_log('MyDingTalk send fail')
        return False

