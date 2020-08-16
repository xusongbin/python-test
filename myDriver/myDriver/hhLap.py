#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct


class Lap(object):
    LAP_CMD_CFRM = 0x00
    LAP_CMD_PCMD = 0x01
    LAP_CMD_GCMD = 0x01
    LAP_CMD_PPAT = 0x02
    LAP_CMD_GPAT = 0x02
    LAP_CMD_SPAT = 0x03
    LAP_CMD_QACK = 0x04
    LAP_CMD_QUERY = 0x04
    LAP_CMD_MODE = 0x05
    LAP_CMD_SMODE = 0x05
    LAP_CMD_SUBCONTRACT = 0x06
    LAP_CMD_DPARAM = 0x07
    LAP_CMD_ERROR = 0x0C
    LAP_CMD_ACKERR = 0x0D
    LAP_CMD_ACKOK = 0x0E
    LAP_CMD_ALERT = 0x0F
    LAP_CMD_SALERT = 0x0F
    LAP_CMD_TEMP = 0x10
    LAP_CMD_STEMP = 0x10
    LAP_CMD_HUM = 0x11
    LAP_CMD_SHUM = 0x11
    LAP_CMD_AP = 0x12
    LAP_CMD_SAP = 0x12
    LAP_CMD_PM25 = 0x13
    LAP_CMD_SPM25 = 0x13
    LAP_CMD_ACC = 0x14
    LAP_CMD_SACC = 0x14
    LAP_CMD_LIGHT = 0x15
    LAP_CMD_SLIGHT = 0x15
    LAP_CMD_CO2 = 0x16
    LAP_CMD_SCO2 = 0x16
    LAP_CMD_VOC = 0x17
    LAP_CMD_SVOC = 0x17
    LAP_CMD_SST = 0x18
    LAP_CMD_SSST = 0x18
    LAP_CMD_LRTEMP = 0x19
    LAP_CMD_SW = 0x20
    LAP_CMD_SSW = 0x20
    LAP_CMD_RELAY = 0x21
    LAP_CMD_SRELAY = 0x21
    LAP_CMD_LADTP = 0x70
    LAP_CMD_VER = 0x90
    LAP_CMD_PS = 0x91
    LAP_CMD_SPS = 0x91
    LAP_CMD_GPS = 0x92
    LAP_CMD_QGPS = 0x92
    LAP_CMD_HRGPS = 0x93
    LAP_CMD_QHRGPS = 0x93
    LAP_CMD_RTC = 0x94
    LAP_CMD_BAT = 0x95
    LAP_CMD_SBAT = 0x95
    LAP_CMD_TIME = 0x96
    LAP_CMD_LRPS = 0x97
    LAP_CMD_FWSIG = 0x9A
    LAP_CMD_DELAY = 0x9C
    LAP_CMD_SDELAY = 0x9C
    LAP_CMD_ULPRD = 0x9D
    LAP_CMD_SULPRD = 0x9D
    LAP_CMD_DLSQ = 0x9E
    LAP_CMD_DINFO = 0x9F
    LAP_CMD_FDEFAULT = 0xA0
    LAP_CMD_USIGNAL = 0xA1
    LAP_CMD_REGRD = 0xAE
    LAP_CMD_REGWR = 0xAF
    LAP_CMD_TEST = 0xFE
    LAP_CMD_CUSTOM = 0xFF

    def __init__(self):
        self.device = {}
        # dd = '9F13323153464530059004012410070A1262001410000C00C100'
        # print(bytes.fromhex(dd))
        # self.parse(bytes.fromhex(dd))
        # print(self.device)

    def parse(self, data):
        if not data:
            return True
        if type(data) != bytes:
            print('Please input bytes')
            return False
        size = len(data)
        index = 0
        while index < size:
            _cmd = data[index]
            index += 1
            if _cmd == self.LAP_CMD_DINFO:
                offset = 8
                if (index + offset) > size:
                    return False
                self.__parse_dinfo(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_VER:
                offset = 3
                if (index + offset) > size:
                    return False
                self.__parse_ver(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_TEMP:
                offset = 2
                if (index + offset) > size:
                    return False
                self.__parse_temp(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_AP:
                offset = 2
                if (index + offset) > size:
                    return False
                self.__parse_ap(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_ACC:
                offset = 6
                if (index + offset) > size:
                    return False
                self.__parse_acc(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_LRTEMP:
                offset = 1
                if (index + offset) > size:
                    return False
                self.__parse_lrtemp(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_FWSIG:
                offset = 4
                if (index + offset) > size:
                    return False
                self.__parse_fwsig(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_LRPS:
                offset = 1
                if (index + offset) > size:
                    return False
                self.__parse_lrps(data[index:index+offset])
                index += offset
            elif _cmd == self.LAP_CMD_REGRD:
                try:
                    data_len = data[index + 2]
                except Exception:
                    return False
                offset = 3 + data_len
                if (index + offset) > size:
                    return False
                self.__parse_regrd(data[index:index+offset])         #len 4~242
                index += offset
            elif _cmd == self.LAP_CMD_ACKERR:
                offset = 1
                if (index + offset) > size:
                    return False
                self.__parse_ackerr(data[index:index + offset])
                index += offset
            elif _cmd == self.LAP_CMD_ACKOK:
                offset = 1
                if (index + offset) > size:
                    return False
                self.__parse_ackok(data[index:index + offset])
                index += offset
            else:
                return False
        return True

    def __parse_dinfo(self, data):
        year, week, name, sub = struct.unpack('BB5sB', data)
        self.device['year'] = year
        self.device['week'] = week
        self.device['name'] = name.decode()
        self.device['sub'] = sub

    def __parse_ver(self, data):
        version = struct.unpack('I', data+b'\x00')[0]
        self.device['lap'] = (version >> 21) & 0x07
        self.device['hard'] = [(version >> 18) & 0x07, (version >> 16) & 0x03]
        self.device['soft'] = [(version >> 12) & 0x0F, (version >> 8) & 0x0F, (version >> 0) & 0xFF]

    def __parse_temp(self, data):
        self.device['temp'] = struct.unpack('h', data)[0] / 100

    def __parse_ap(self, data):
        self.device['ap'] = struct.unpack('H', data)[0]

    def __parse_acc(self, data):
        self.device['acc'] = [int(x / 16) for x in struct.unpack('<hhh', data)]
        self.device['acc_g'] = 0
        self.device['acc_g'] += pow(self.device['acc'][0], 2)
        self.device['acc_g'] += pow(self.device['acc'][1], 2)
        self.device['acc_g'] += pow(self.device['acc'][2], 2)
        self.device['acc_g'] = int(self.device['acc_g'] ** 0.5)
    def __parse_lrtemp(self,data):
        self.device['lr_temp'] = struct.unpack('b', data)[0]
    def __parse_fwsig(self,data):
        fw_sig_big_endian = data[::-1]
        self.device['fw_sig'] = fw_sig_big_endian.hex()
    def __parse_lrps(self,data):
        self.device['lr_ps'] = (struct.unpack('B', data)[0] + 180) * 10    #unit:1mv
    def __parse_regrd(self,data):
        parse_len = len(data)
        if parse_len < 3:
            return
        data_len = data[2]
        if parse_len != (3 + data_len):
            return
        addr_key = 'addr'
        len_key = 'len'
        data_key = 'data'
        addr_index = 1
        len_index = 1
        data_index = 1
        if addr_key in self.device:
            addr_key += str(addr_index)
        if len_key in self.device:
            len_key += str(len_index)
        if data_key in self.device:
            data_key += str(data_index)
        self.device[addr_key] = struct.unpack('<H', data[:2])[0]
        self.device[len_key] = data[2]
        self.device[data_key] = data[3:]
    def __parse_ackerr(self,data):
        self.device['ack_err_cmd'] = struct.unpack('<B', data)[0]
    def __parse_ackok(self,data):
        self.device['ack_ok_cmd'] = struct.unpack('<B', data)[0]
    def prepare(self, cmd, data):
        if cmd == self.LAP_CMD_REGWR:
            if not isinstance(data, dict):
                return None
            if not 'addr' in data:
                return None
            if not 'len' in data:
                return None
            if not 'data' in data:
                return None
            hex_bytes = b''
            hex_bytes += cmd.to_bytes(1, byteorder='little')
            hex_bytes += data['addr'].to_bytes(2, byteorder='little')
            hex_bytes += data['len'].to_bytes(1, byteorder='little')
            hex_bytes += data['data']
            return hex_bytes
        elif cmd == self.LAP_CMD_REGRD:
            if not isinstance(data, dict):
                return None
            if not 'addr' in data:
                return None
            if not 'len' in data:
                return None
            hex_bytes = b''
            hex_bytes += struct.pack('<B', cmd)
            hex_bytes += struct.pack('<H', data['addr'])
            hex_bytes += struct.pack('<B', data['len'])
            return hex_bytes