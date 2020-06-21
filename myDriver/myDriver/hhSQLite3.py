#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from traceback import format_exc

from myDriver.hhLog import write_log


class SQLite3(object):
    def __init__(self, database):
        self.__conn = sqlite3.connect(database, check_same_thread=False)

    def execute(self, content):
        try:
            if content.find('SELECT') == 0 or content.find('PRAGMA') == 0:
                return self.__conn.cursor().execute(content).fetchall()
            self.__conn.cursor().execute(content)
            return True
        except Exception as e:
            write_log(content)
            write_log('EXECUTE except:{}\n{}'.format(e, format_exc()))
        return False

    def commit(self):
        self.__conn.commit()

    def exist(self, table_name):
        content = '{} COUNT(*) FROM sqlite_master WHERE type=\'table\' and name=\'{}\''.format('SELECT', table_name)
        data = self.execute(content)
        try:
            if data[0][0] == 1:
                return True
        except Exception as e:
            write_log('EXIST except:{}\n{}'.format(e, format_exc()))
        return False

    def create(self, _type, name, item_form):
        content = '{} {} {} {}'.format('CREATE', _type, name, item_form)
        return self.execute(content)

    def drop(self, table_name, table_item):
        content = '{} {} {}'.format('DROP', table_name, table_item)
        return self.execute(content)

    def insert(self, table_name, table_item, item_data):
        content = '{} INTO {}({}) VALUES({})'.format('INSERT', table_name, table_item, item_data)
        return self.execute(content)

    def update(self, table_name, table_item, item_data, data_limit=''):
        content = '{} {} SET ({}) = ({})'.format('UPDATE', table_name, table_item, item_data)
        if data_limit:
            content += ' WHERE %s' % data_limit
        return self.execute(content)

    def replace(self, table_name, table_item, item_data):
        content = '{} INTO {}({}) VALUES({})'.format('REPLACE', table_name, table_item, item_data)
        return self.execute(content)

    def delete(self, table_name, table_item, item_data):
        content = '{} FROM {} WHERE {}={}'.format('DELETE', table_name, table_item, item_data)
        return self.execute(content)

    def select(self, table_name, table_item, data_limit=None):
        content = '{} {} FROM {}'.format('SELECT', table_item, table_name)
        if data_limit:
            content += ' WHERE %s' % data_limit
        return self.execute(content)

    def info(self, table_name):
        if not self.exist(table_name):
            return None
        content = 'PRAGMA table_info("{}")'.format(table_name)
        return self.execute(content)

    def item(self, table_name):
        _info = self.info(table_name)
        if not _info:
            return None
        return [x[1] for x in _info]

    def table_create(self, table_name, table_item, seq=False):
        _form_list = ['{} {}'.format(x, 'VARCHAR' if x != 'TIME' else 'DATETIME') for x in table_item]
        if seq:
            _form_list.append('SEQ INTEGER PRIMARY KEY AUTOINCREMENT')
        else:
            _form_list[0] = '{} PRIMARY KEY'.format(_form_list[0])
        _form = '({});'.format(','.join(_form_list))
        return self.create('TABLE', table_name, _form)

    def table_check(self, table_name, table_item, seq=False):
        if self.exist(table_name):
            return True
        return self.table_create(table_name, table_item, seq)

    def table_select(self, table_name, table_item, table_limit=None):
        return self.select(table_name, ','.join(table_item), table_limit)

    def table_replace(self, table_name, table_data):
        _item = self.item(table_name)
        if len(_item) != len(table_data):
            raise Exception('table_replace data length does not match table item')
        if type(table_data) == list:
            table_data = ','.join(["'{}'".format(x) for x in table_data])
        _table_item = ','.join(_item)
        return self.replace(table_name, _table_item, table_data)

    def table_insert(self, table_name, table_data):
        _item = self.item(table_name)
        if _item[-1] == 'SEQ':
            if len(_item)-1 != len(table_data):
                raise Exception('table_insert data length does not match table item')
            if type(table_data) == list:
                table_data = ','.join(["'{}'".format(x) for x in table_data])
            _table_item = ','.join(_item[:-1])
            return self.insert(table_data, _table_item, table_data)
        else:
            if len(_item) != len(table_data):
                raise Exception('table_insert data length does not match table item')
            if type(table_data) == list:
                table_data = ','.join(["'{}'".format(x) for x in table_data])
            _table_item = ','.join(_item)
            return self.insert(table_data, _table_item, table_data)

    def table_default(self, table_name, table_item, table_data):
        if self.table_select(table_name, table_item):
            return True
        self.table_replace(table_name, table_data)

    def table_distinct(self, table_name, table_para):
        _result = self.select(table_name, 'DISTINCT {}'.format(table_para))
        if not _result:
            return None
        return _result[0]

    def table_time(self, table_name, method='MIN'):
        try:
            return self.select(table_name, '{}(TIME)'.format(method))[0][0]
        except Exception as e:
            _ = e
        return None


if __name__ == '__main__':
    _sql = SQLite3('test.db')
    # print(_sql.exist('RHF1S05X_STEP1_CONFIG'))
    print(_sql.item('RHF1S05X_STEP1_CONFIG'))
    # table_data = ','.join(["'{}'".format(x) for x in ['asd', '-55']])
    # print(table_data)
