#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep, time
from myDriver.hhSerial import Serial
from myDriver.hhLog import write_log


class Atm(object):
    MAGIC = '"{RXHF)&=;"'
    __ERROR = 'ERROR'
    __AT = 'AT'
    __RESET = 'RESET'
    __FDEFAULT = 'FDEFAULT'
    __DFU = 'DFU'
    __LOWPOWER = 'LOWPOWER'
    __VER = 'VER'
    __MSG = 'MSG'
    __CMSG = 'CMSG'
    __PMSG = 'PMSG'
    __MSGHEX = 'MSGHEX'
    __CMSGHEX = 'CMSGHEX'
    __PMSGHEX = 'PMSGHEX'
    __CH = 'CH'
    __ADR = 'ADR'
    __DR = 'DR'
    __REPT = 'REPT'
    __RETRY = 'RETRY'
    __POWER = 'POWER'
    __RXWIN1 = 'RXWIN1'
    __RXWIN2 = 'RXWIN2'
    __PORT = 'PORT'
    __MODE = 'MODE'
    __ID = 'ID'
    __KEY = 'KEY'
    __CLASS = 'CLASS'
    __JOIN = 'JOIN'
    __LW = 'LW'
    __BEACON = 'BEACON'
    __TEST = 'TEST'
    __UART = 'UART'
    __DELAY = 'DELAY'
    __VDD = 'VDD'
    __RTC = 'RTC'
    __EEPROM = 'EEPROM'
    __WDT = 'WDT'
    __TEMP = 'TEMP'
    __REG = 'REG'
    __LOG = 'LOG'
    __IRQ = 'IRQ'
    __SYS = 'SYS'
    __FDB = 'FDB'
    __RELAY = 'RELAY'

    def __init__(self, com='COM1', rate=9600, log=False):
        self.serial = Serial(com, rate, wakeup=True, alog=log)

    def reset_port(self, com):
        self.serial.reset_describe(com)

    def reset_rate(self, rate):
        self.serial.reset_rate(rate)

    def wait_open(self):
        while not self.serial.get_port_open():
            sleep(0.1)

    def receive(self, tout):
        return self.serial.get(tout)

    def check_error(self, data):
        if not data:
            return True
        if self.__ERROR in data:
            return True
        return False

    def at(self):
        _tx = '{}'.format(self.__AT)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__AT))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__AT)+2:].strip()

    def at_fdefault(self):
        _tx = '{}+{}'.format(self.__AT, self.__FDEFAULT)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}:  .*'.format(self.__FDEFAULT), 1000)
        if self.check_error(_recv):
            return None
        return _recv[len(self.__FDEFAULT)+2:].strip()

    def at_reset(self):
        _tx = '{}+{}'.format(self.__AT, self.__RESET)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__RESET), 8000)
        if self.check_error(_recv):
            return None
        return _recv[len(self.__RESET)+2:].strip()

    def at_dfu(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__DFU)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__DFU))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__DFU) + 2:].strip()

    def at_lowpower(self, para='AUTOON'):
        _tx = '{}+{}'.format(self.__AT, self.__LOWPOWER)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__LOWPOWER))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__LOWPOWER) + 2:].strip()

    def at_ver(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__VER)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__VER))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__VER) + 2:].strip()

    def at_msg_api(self, para=None, cmd=None):
        if not cmd:
            cmd = self.__MSG
        _tx = '{}+{}'.format(self.__AT, cmd)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _list = []
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: Start$'.format(cmd))
        if self.check_error(_recv):
            return None
        while True:
            _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(cmd), 5000)
            if self.check_error(_recv):
                return None
            if 'Done' in _recv:
                break
            _list.append(_recv[len(cmd) + 2:].strip())
        return _list

    def at_msg(self, para=None):
        return self.at_msg_api(para, self.__MSG)

    def at_msghex(self, para=None):
        return self.at_msg_api(para, self.__MSGHEX)

    def at_cmsg(self, para=None):
        return self.at_msg_api(para, self.__CMSG)

    def at_cmsghex(self, para=None):
        return self.at_msg_api(para, self.__CMSGHEX)

    def at_pmsg(self, para=None):
        return self.at_msg_api(para, self.__PMSG)

    def at_pmsghex(self, para=None):
        return self.at_msg_api(para, self.__PMSGHEX)

    def at_ch(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__CH)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__CH))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__CH) + 2:].strip()

    def at_adr(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__ADR)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__ADR))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__ADR) + 2:].strip()

    def at_dr(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__DR)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__DR))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__DR) + 2:].strip()

    def at_rept(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__REPT)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__REPT))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__REPT) + 2:].strip()

    def at_retry(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__RETRY)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__RETRY))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__RETRY) + 2:].strip()

    def at_power(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__POWER)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__POWER))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__POWER) + 2:].strip()

    def at_rxwin1(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__RXWIN1)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__RXWIN1))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__RXWIN1) + 2:].strip()

    def at_rxwin2(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__RXWIN2)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__RXWIN2))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__RXWIN2) + 2:].strip()

    def at_port(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__PORT)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__PORT))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__PORT) + 2:].strip()

    def at_mode(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__MODE)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__MODE))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__MODE) + 2:].strip()

    def at_id(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__ID)
        if para:
            _tx = '{}={}'.format(_tx, para)
            _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__ID))
            if self.check_error(_recv):
                return None
            return _recv[len(self.__ID) + 2:].strip()
        else:
            _data = {'DEVADDR': '', 'DEVEUI': '', 'APPEUI': ''}
            _recv = self.serial.send_wait_regular(_tx, r'^\+{}: DevAddr, .*'.format(self.__ID))
            if self.check_error(_recv):
                return None
            _data['DEVADDR'] = _recv[len(self.__ID) + 2 + 7 + 2:].strip()
            _recv = self.serial.send_wait_regular(_tx, r'^\+{}: DevEui, .*'.format(self.__ID))
            if self.check_error(_recv):
                return None
            _data['DEVEUI'] = _recv[len(self.__ID) + 2 + 6 + 2:].strip()
            _recv = self.serial.send_wait_regular(_tx, r'^\+{}: AppEui, .*'.format(self.__ID))
            if self.check_error(_recv):
                return None
            _data['APPEUI'] = _recv[len(self.__ID) + 2 + 6 + 2:].strip()
            return _data

    def at_key(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__KEY)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__KEY))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__KEY) + 2:].strip()

    def at_class(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__CLASS)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__CLASS))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__CLASS) + 2:].strip()

    def at_join(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__JOIN)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__JOIN), 10000)
        if self.check_error(_recv):
            return None
        if 'Not in OTAA mode' in _recv:
            return _recv[len(self.__JOIN) + 2:].strip()
        if 'Joined already' in _recv:
            return _recv[len(self.__JOIN) + 2:].strip()
        if 'Start' in _recv:
            _list = []
            while True:
                _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__JOIN), 10000)
                if self.check_error(_recv):
                    return None
                if 'Done' in _recv:
                    break
                _list.append(_recv[len(self.__JOIN) + 2:].strip())
            return _list
        return None

    def at_lw(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__LW)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__LW))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__LW) + 2:].strip()

    def at_beacon(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__BEACON)
        if para:
            _tx = '{}={}'.format(_tx, para)
            if 'PSDEBUG' == para:
                _list = []
                self.serial.send(_tx)
                ts = time()
                while (time()-ts) < 0.5:
                    _recv = self.serial.get(0.1)
                    if not _recv:
                        break
                    if '+BEACON: OK' in _recv:
                        break
                    _list.append(_recv)
                return _list
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__BEACON))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__BEACON) + 2:].strip()

    def at_test(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__TEST)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__TEST))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__TEST) + 2:].strip()

    def at_uart(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__UART)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__UART))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__UART) + 2:].strip()

    def at_vdd(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__VDD)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__VDD))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__VDD) + 2:].strip()

    def at_rtc(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__RTC)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__RTC))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__RTC) + 2:].strip()

    def at_eeprom(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__EEPROM)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__EEPROM))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__EEPROM) + 2:].strip()

    def at_wdt(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__WDT)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__WDT))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__WDT) + 2:].strip()

    def at_temp(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__TEMP)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__TEMP))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__TEMP) + 2:].strip()

    def at_reg(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__REG)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__REG))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__REG) + 2:].strip()

    def at_log(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__LOG)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__LOG))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__LOG) + 2:].strip()

    def at_irq(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__IRQ)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__IRQ))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__IRQ) + 2:].strip()

    def at_sys(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__SYS)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__SYS))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__SYS) + 2:].strip()

    def at_delay(self, para=None):
        _tx = '{}+{}'.format(self.__AT, self.__DELAY)
        if para:
            _tx = '{}={}'.format(_tx, para)
        _recv = self.serial.send_wait_regular(_tx, r'^\+{}: .*'.format(self.__DELAY))
        if self.check_error(_recv):
            return None
        return _recv[len(self.__DELAY) + 2:].strip()


if __name__ == '__main__':
    atm = Atm('COM66', log=True)
    atm.wait_open()
    print(atm.at_class())
