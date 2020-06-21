#!/usr/bin/env python
# -*- coding: utf-8 -*-

# You need to add the path to the system environment
# path:E:\Program Files\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility

import os
import re
import subprocess
from traceback import format_exc
from time import sleep

from myDriver.hhLog import write_log

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE


class StLink(object):
    __cmd_connect = '-c port=SWD reset=HWrst'
    __cmd_erase_chip = '-e all'
    __cmd_download = '-d'
    __cmd_option_byte = '-ob'
    __cmd_start = '--start'
    __cmd_reset = '--rst'

    def __init__(self, path='STM32_Programmer_CLI', log=True):
        self.path = path
        self.log = log

    def run(self, cmd):
        data = ''
        tx = '{} {}'.format(self.path, cmd)
        write_log('CMD tx:' + tx)
        try:
            resp = subprocess.Popen(tx, stdout=subprocess.PIPE, startupinfo=startupinfo)
            recv, err = resp.communicate()
            for dat in recv.decode('utf-8', 'ignore').split('\n'):
                dat = dat.strip()
                if not dat:
                    continue
                data += dat + '\n'
                write_log('CMD rx:' + dat)
            return str(data)
        except Exception as e:
            write_log('run except:%s' % e)
        return None

    def test(self):
        respond = os.popen('{} {}'.format(self.path, self.__cmd_connect)).read()
        print(respond)

    def connect(self):
        cmd = self.__cmd_connect
        respond = self.run(cmd)
        return respond

    def erase_chip(self):
        cmd = self.__cmd_connect
        cmd += ' {}'.format(self.__cmd_erase_chip)
        respond = self.run(cmd)
        if 'Mass erase successfully achieved' in respond:
            write_log('Erase chip done.')
            return True
        write_log('Erase chip except.')
        return False

    def program(self, file, addr='0x08000000'):
        cmd = self.__cmd_connect
        cmd += ' {}'.format(self.__cmd_download)
        if '.bin' in file:
            cmd += ' {} {}'.format(file, addr)
        else:
            cmd += ' {}'.format(file)
        respond = self.run(cmd)
        print(respond)
        try:
            if 'File download complete' in respond:
                return True
        except Exception as e:
            print('{}\n{}'.format(e, format_exc()))
        return False

    def read_protect(self):
        cmd = self.__cmd_connect
        cmd += ' {}'.format(self.__cmd_option_byte)
        cmd += ' {}'.format('displ')
        respond = self.run(cmd)
        find = re.findall(r'(RDP.*0x[0-9A-F]+)', respond)
        if len(find) == 0:
            return False
        rdp = str(find[0]).split('x')[1][:2]
        return rdp

    def write_protect(self, rdp='0xBB'):
        cmd = self.__cmd_connect
        cmd += ' {}'.format(self.__cmd_option_byte)
        cmd += ' RDP={}'.format(rdp)
        respond = self.run(cmd)
        if 'Option Bytes successfully programmed' in respond:
            return True
        if 'Option Byte: rdp, value: 0xAA, was not modified' in respond:
            return True
        return False

    def start(self):
        cmd = self.__cmd_connect
        cmd += ' {}'.format(self.__cmd_start)
        cmd += ' {}'.format('0x08000000')
        self.run(cmd)

    def reset(self):
        cmd = self.__cmd_connect
        cmd += ' {}'.format(self.__cmd_reset)
        self.run(cmd)

    def rewrite_fimware(self, firmware, protect=True, lock=True):
        if lock:
            self.write_protect()
        if not self.write_protect('0xAA'):
            return False
        if not self.program(firmware):
            return False
        if protect:
            self.write_protect()
        else:
            self.start()
        return True


def batch_loading():
    _st = StLink()
    _path = 'E:/GIT/firmware-merge-tool/RHF0M003-FE1/v1.2.8-20200425/RHF1SFE0-v1.2.8-20200425-allinone.hex'
    while True:
        sta = _st.rewrite_fimware(_path, True, False)
        if sta:
            while _st.read_protect():
                pass
        sleep(1)


if __name__ == '__main__':
    # cmd = "STM32_Programmer_CLI -c port=SWD reset=HWrst -d E:/GIT/firmware-merge-tool/RHF0M055/v1.1.0-20200408/rhf0m055-v1.1.0-20200408-allinone.hex"
    # firmware = r'C:\Users\Administrator\Desktop\rhf0m055-v0.0.9-20191223-allinone.hex'
    # firmware = r'E:\Development\项目资料\RHF76-052-JRI\测试固件\LoRa_JRI_2020-04-01.hex'
    # st = StLink()
    # st.rewrite_fimware(firmware, False)
    batch_loading()
