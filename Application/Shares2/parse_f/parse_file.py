#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import strftime, localtime


class ParseFile(object):
    def __init__(self):
        pass

    @staticmethod
    def parse_time(_time):
        _year = (_time & 0xFFF00000) >> 20
        _month = (_time & 0x000F0000) >> 16
        _day = (_time & 0x0000F800) >> 11
        _hour = (_time & 0x000007C0) >> 6
        _min = (_time & 0x0000003F) >> 0
        return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(_year+1900, _month, _day, _hour, _min, 0)

    def parse_file(self, file, digit=2):
        print(file)
        with open(file, 'rb') as f:
            byte_array = f.read()
        if not byte_array:
            return False
        _file_len = len(byte_array)
        _identify = byte_array[0:6].decode()
        _record_num = int.from_bytes(byte_array[6:10], byteorder='little')
        _record_start = int.from_bytes(byte_array[10:12], byteorder='little')
        _record_len = int.from_bytes(byte_array[12:14], byteorder='little')
        _column_num = int.from_bytes(byte_array[14:16], byteorder='little')
        print('total:{} {} num:{} start:{} len:{} column:{}'.format(
            _file_len, _identify, _record_num, _record_start, _record_len, _column_num
        ))
        # for i in range(16, _record_start, 4):
        #     print('{}\t{}'.format(i, int.from_bytes(byte_array[i:i+2], byteorder='little')))
        # return
        _column_data = byte_array[_record_start:]
        _column_per = int(_record_len/_column_num)

        _skip = True
        _skip_num = 0
        for i in range(0, _file_len - _record_start, _record_len):
            _time = int.from_bytes(_column_data[i+0:i+4], byteorder='little')
            _open = int.from_bytes(_column_data[i+4:i+8], byteorder='little')
            _high = int.from_bytes(_column_data[i+8:i+12], byteorder='little')
            _low = int.from_bytes(_column_data[i+12:i+16], byteorder='little')
            _close = int.from_bytes(_column_data[i+16:i+20], byteorder='little')
            _value = int.from_bytes(_column_data[i+20:i+24], byteorder='little')
            _volume = int.from_bytes(_column_data[i+24:i+28], byteorder='little')
            # parse
            # 计算时间点
            _time_str = self.parse_time(_time)
            # TODO: maybe more than 0xC0000000
            _out_open = (_open & 0x0FFFFFFF) * pow(10, 8 - (_open >> 28))
            _out_high = (_high & 0x0FFFFFFF) * pow(10, 8 - (_high >> 28))
            _out_low = (_low & 0x0FFFFFFF) * pow(10, 8 - (_low >> 28))
            _out_close = (_close & 0x0FFFFFFF) * pow(10, 8 - (_close >> 28))
            # TODO: maybe more than 0x20000000
            _value = 0 if _value == 0xFFFFFFFF else _value
            _out_value = int((_value & 0x0FFFFFFF) * pow(10, (_value >> 28)))
            # TODO: maybe more than 0x10000000
            _volume = 0 if _volume == 0xFFFFFFFF else _volume
            _out_volume = int((_volume & 0x0FFFFFFF) * pow(10, (_volume >> 28) - 2))
            _show_str = '{} open:{:.%df} high:{:.%df} low:{:.%df} close:{:.%df} value:{} volume:{}' % (
                digit, digit, digit, digit
            )
            print(_show_str.format(_time_str, _out_open, _out_high, _out_low, _out_close, _out_value, _out_volume))
            # print('{} open:{:8X} high:{:8X} low:{:8X} close:{:8X} value:{:8X} volume:{:8X}'.format(
            #     _time_str, _open, _high, _low, _close, _value, _volume
            # ))

    def parse_1a0001(self):
        _file_name = r'C:\同花顺软件\同花顺\history\shase\min5\1A0001.mn5'
        self.parse_file(_file_name, 2)

    def parse_881155(self):
        _file_name = r'C:\同花顺软件\同花顺\history\newindx\min5\881155.mn5'
        self.parse_file(_file_name, 3)

    def parse_usdcnh(self):
        _file_name = r'C:\同花顺软件\同花顺\history\foreign\min5\USDCNH.mn5'
        self.parse_file(_file_name, 5)


if __name__ == '__main__':
    fp = ParseFile()
    fp.parse_1a0001()
    # fp.parse_881155()
    # fp.parse_usdcnh()
