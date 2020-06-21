#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from traceback import format_exc

import xlwt
import xlrd

from myDriver.hhLog import write_log


class Excel(object):
    def write(self, file, head, lines):
        filename, suffix = os.path.splitext(file)
        if suffix == '.xls':
            return self.__write_xlwt(file, head, lines)
        return False

    def read(self, file, page=0):
        return self.__read_xlrd(file, page)

    @staticmethod
    def __write_xlwt(file, head, lines):
        row = 0
        row_cnt = 0
        try:
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('Sheet1')
            for col, data in enumerate(head.split(',')):
                worksheet.write(row, col, data)
            for line in lines:
                if (row_cnt % 50000) == 0 and row_cnt > 0:
                    row = 0
                    worksheet = workbook.add_sheet('Sheet{}'.format(int(row_cnt / 50000) + 1))
                    for col, data in enumerate(head.split(',')):
                        worksheet.write(row, col, data)
                row += 1
                row_cnt += 1
                for col, data in enumerate(line):
                    if col >= len(head.split(',')):
                        continue
                    worksheet.write(row, col, data)
            workbook.save(file)
        except Exception as e:
            write_log('XLWT except:{}\n{}'.format(e, format_exc()))
            return False
        return True

    @staticmethod
    def __read_xlrd(file, page=0):
        _list = []
        try:
            workbook = xlrd.open_workbook(file)
            worksheet = workbook.sheet_by_index(page)
            for i in range(worksheet.nrows):
                _list.append(worksheet.row_values(i))
        except Exception as e:
            write_log('XLRD except:{}\n{}'.format(e, format_exc()))
        if not len(_list) > 0:
            return False
        return _list
