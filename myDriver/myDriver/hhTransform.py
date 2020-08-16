#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import struct


class Transform(object):

    @staticmethod
    def ascii_to_int(data):
        return ord(data)

    @staticmethod
    def int_to_ascii(data):
        return chr(data)

    @staticmethod
    def dec_to_hex(data):
        if type(data) is not int:
            raise Exception('input is not int')
        return hex(data)

    def hex_to_dec(self, data, little=False):
        if not re.match(r'(0[xX])?[0-9A-Fa-f]+', data):
            raise Exception('input is not hex')
        if little:
            data = self.str_to_bytes(data)
            return self.byte_to_int(data, sign=False)
        return int(data, 16)

    @staticmethod
    def byte_to_char(data, sign=True):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 1:
            raise Exception('input bytes length is not 1')
        if sign:
            fmt = 'b'
        else:
            fmt = 'B'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def byte_to_bool(data):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 1:
            raise Exception('input bytes length is not 1')
        fmt = '?'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def byte_to_short(data, order='little', sign=True):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 2:
            raise Exception('input bytes length is not 2')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'h'
        else:
            fmt += 'H'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def byte_to_int(data, order='little', sign=True):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'i'
        else:
            fmt += 'I'
        if len(data) == 4:
            return struct.unpack('{}'.format(fmt), bytes(data))[0]
        elif len(data) == 8:
            _h = struct.unpack('{}'.format(fmt), bytes(data[:4]))[0]
            _l = struct.unpack('{}'.format(fmt), bytes(data[4:]))[0]
            if order == 'big':
                return _h * 0xFFFFFFFF + _l
            else:
                return _l * 0xFFFFFFFF + _h
        raise Exception('input bytes length is not 4')

    @staticmethod
    def byte_to_long(data, order='little', sign=True):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 4:
            raise Exception('input bytes length is not 4')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'l'
        else:
            fmt += 'L'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def byte_to_longlong(data, order='little', sign=True):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 8:
            raise Exception('input bytes length is not 8')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'q'
        else:
            fmt += 'Q'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def byte_to_float(data):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 4:
            raise Exception('input bytes length is not 4')
        fmt = 'f'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def byte_to_double(data):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        if len(data) != 8:
            raise Exception('input bytes length is not 8')
        fmt = 'd'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

    @staticmethod
    def char_to_bytes(data, sign=True):
        if type(data) is not int:
            raise Exception('input is not int')
        if sign:
            fmt = 'b'
        else:
            fmt = 'B'
        return struct.pack('{}'.format(fmt), data)

    @staticmethod
    def short_to_bytes(data, order='little', sign=True):
        if type(data) is not int:
            raise Exception('input is not int')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'h'
        else:
            fmt += 'H'
        return struct.pack('{}'.format(fmt), data)

    @staticmethod
    def int_to_bytes(data, order='little', sign=True):
        if type(data) is not int:
            raise Exception('input is not int')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'i'
        else:
            fmt += 'I'
        return struct.pack('{}'.format(fmt), data)

    @staticmethod
    def longlong_to_bytes(data, order='little', sign=True):
        if type(data) is not int:
            raise Exception('input is not int')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'q'
        else:
            fmt += 'Q'
        return struct.pack('{}'.format(fmt), data)

    @staticmethod
    def bytes_to_hex(data):
        if type(data) is not bytes:
            raise Exception('input is not bytes')
        size = len(data)
        return data.hex().rjust(size*2, '0')

    @staticmethod
    def str_to_bytes(data):
        if re.match(r'0[xX][0-9A-Fa-f]+', data):
            data = data.upper().split('X')[1]
        if not re.match(r'[0-9A-Fa-f]+', data):
            raise Exception('input is not string')
        return bytes.fromhex(data)


if __name__ == '__main__':
    tf = Transform()
    # print(tf.byte_to_longlong(b'\x00\x00\x00\x00\x00\x00\x00\x80', order='little', sign=False))
    # print(tf.byte_to_bool(b'\x02'))
    # print(tf.byte_to_float(b'\x00\x00\x00\x01'))
    print(tf.short_to_bytes(154))
    # print(tf.dec_to_sign_dec(0xFF))
    # print(hex(tf.sign_dec_to_dec(-1)))
    # print(tf.bytes_to_hex(b'\x00\x02'))
