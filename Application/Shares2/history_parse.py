#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from my_driver import *


class ParseFile(object):
    path_1A0001 = r'C:\同花顺软件\同花顺\history\shase\min5\1A0001.mn5'
    path_399001 = r'C:\同花顺软件\同花顺\history\sznse\min5\399001.mn5'
    path_881155 = r'C:\同花顺软件\同花顺\history\newindx\min5\881155.mn5'
    path_USDCNH = r'C:\同花顺软件\同花顺\history\foreign\min5\USDCNH.mn5'
    digit_1A0001 = 2
    digit_399001 = 2
    digit_881155 = 3
    digit_USDCNH = 5

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

    def parse_file(self, file, digit, num, delete):
        with open(file, 'rb') as f:
            byte_array = f.read()
        try:
            if delete:
                os.remove(file)
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        if not byte_array:
            return False
        write_log('Parse ')
        _total_len = len(byte_array)
        # _identify = byte_array[0:6].decode()
        _record_num = int.from_bytes(byte_array[6:10], byteorder='little')
        _record_start = int.from_bytes(byte_array[10:12], byteorder='little')
        _record_len = int.from_bytes(byte_array[12:14], byteorder='little')
        # _column_num = int.from_bytes(byte_array[14:16], byteorder='little')

        _data_array = byte_array[_record_start:]
        _data_len = len(_data_array)
        if num > _record_num:
            _num_get = _record_num
        else:
            _num_get = num
        _idx_stop = _total_len - _record_start
        _idx_start = _data_len - _num_get * _record_len
        _idx_step = _record_len

        _data_list = []
        for i in range(_idx_start, _idx_stop, _idx_step):
            _time = int.from_bytes(_data_array[i+0:i+4], byteorder='little')
            _open = int.from_bytes(_data_array[i+4:i+8], byteorder='little')
            _high = int.from_bytes(_data_array[i+8:i+12], byteorder='little')
            _low = int.from_bytes(_data_array[i+12:i+16], byteorder='little')
            _close = int.from_bytes(_data_array[i+16:i+20], byteorder='little')
            _value = int.from_bytes(_data_array[i+20:i+24], byteorder='little')
            _volume = int.from_bytes(_data_array[i+24:i+28], byteorder='little')
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
            _data_list.append([_time_str, _out_open, _out_high, _out_low, _out_close, _out_value, _out_volume])
            # print('{} open:{:8X} high:{:8X} low:{:8X} close:{:8X} value:{:8X} volume:{:8X}'.format(
            #     _time_str, _open, _high, _low, _close, _value, _volume
            # ))
        return np.array(_data_list)

    def parse_1a0001(self, num=100000, delete=False):
        write_log('Parse {} {}'.format('1A0001', num))
        return self.parse_file(self.path_1A0001, self.digit_1A0001, num, delete)

    def parse_399001(self, num=100000, delete=False):
        write_log('Parse {} {}'.format('399001', num))
        return self.parse_file(self.path_399001, self.digit_399001, num, delete)

    def parse_881155(self, num=100000, delete=False):
        write_log('Parse {} {}'.format('881155', num))
        return self.parse_file(self.path_881155, self.digit_881155, num, delete)

    def parse_usdcnh(self, num=100000, delete=False):
        write_log('Parse {} {}'.format('USDCNH', num))
        return self.parse_file(self.path_USDCNH, self.digit_USDCNH, num, delete)

    def parse_1a0001_value(self, num=7, delete=False):
        write_log('Parse {} {}'.format('1A0001', num))
        _data = self.parse_file(self.path_1A0001, self.digit_1A0001, num, delete)
        if len(_data) != 7:
            return False
        _time = _data[-2][0]
        if not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:(00|30):00', _time):
            return False
        _value = 0
        for i in range(6):
            _value += int(_data[i][-2])
        return [_time, _value]

    def parse_399001_value(self, num=7, delete=False):
        write_log('Parse {} {}'.format('399001', num))
        _data = self.parse_file(self.path_399001, self.digit_399001, num, delete)
        if len(_data) != 7:
            return False
        _time = _data[-2][0]
        if not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:(00|30):00', _time):
            return False
        _value = 0
        for i in range(6):
            _value += int(_data[i][-2])
        return [_time, _value]


if __name__ == '__main__':
    fp = ParseFile()
    print(fp.parse_1a0001_value())
    # fp.parse_881155()
    # fp.parse_usdcnh()
