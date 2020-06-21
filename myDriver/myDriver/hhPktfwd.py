#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import queue
import struct
from time import time

from myDriver.hhLog import write_log
from myDriver.hhFile import File


class Pktfwd(object):
    __cmd_push_data = 0x00
    __cmd_push_ack = 0x01
    __cmd_pull_data = 0x02
    __cmd_pull_resp = 0x03
    __cmd_pull_ack = 0x04
    __cmd_tx_ack = 0x05
    # PUSH DATA: Return ACK 0x01
    # PULL DATA: Return ACK 0x04    After PULL_RESP 0x03
    __pktfwd_delay = 0.2    # second

    def __init__(self):
        self.__file = File()

        self.queue_rx = queue.Queue()
        self.queue_tx = queue.Queue()

    def rx_pop(self):
        if self.queue_rx.empty():
            return None
        return self.queue_rx.get()

    def tx_pop(self):
        if self.queue_tx.empty():
            return None
        data, times = self.queue_tx.get()
        if times and (time() - times) < self.__pktfwd_delay:
            # Delay to send to gw
            self.queue_tx.put((data, times))
            return None
        return data

    def __tx_put(self, data, times=None):
        self.queue_tx.put((data, times))

    def __push_data(self, data):
        _protocol = data[:12]
        _recv = json.loads(data[12:].decode())
        for key in _recv.keys():
            if 'stat' == key:
                pass
            elif 'rxpk' == key:
                for _pkt in _recv[key]:
                    _data = self.__file.base64_decode(_pkt['data'], True)
                    _rxpkt = {
                        'protocol': _protocol,
                        'data': _data,
                        'freq': _pkt['freq'],
                        'rssi': _pkt['rssi'],
                        'lsnr': _pkt['lsnr'],
                        'datr': _pkt['datr'],
                        'codr': _pkt['codr'],
                    }
                    self.queue_rx.put(_rxpkt)

    def pack(self, rxpkt, data, **keyword):
        if type(data) is not bytes:
            raise Exception('PKTFWD pack_tx need bytes')
        _imme = True
        if 'imme' in keyword.keys():
            _imme = keyword['imme']
        _freq = rxpkt['freq']
        if 'freq' in keyword.keys():
            _freq = keyword['freq']
        _rfch = 0
        if 'rfch' in keyword.keys():
            _rfch = keyword['rfch']
        _powe = 14
        if 'powe' in keyword.keys():
            _powe = keyword['powe']
        _modu = 'LORA'
        if 'modu' in keyword.keys():
            _modu = keyword['modu']
        _datr = 'SF7BW125'
        if 'datr' in keyword.keys():
            _datr = keyword['datr']
        _codr = '4/5'
        if 'codr' in keyword.keys():
            _codr = keyword['codr']
        _ipol = False
        if 'ipol' in keyword.keys():
            _ipol = keyword['ipol']
        send = {'txpk': {}}
        send['txpk']['imme'] = _imme
        send['txpk']['freq'] = _freq
        send['txpk']['rfch'] = _rfch
        send['txpk']['powe'] = _powe
        send['txpk']['modu'] = _modu
        send['txpk']['datr'] = _datr
        send['txpk']['codr'] = _codr
        send['txpk']['ipol'] = _ipol
        send['txpk']['size'] = len(data)
        send['txpk']['data'] = self.__file.base64_encode(data)
        _pull_resp = rxpkt['protocol'][:3]
        _pull_resp += struct.pack('B', self.__cmd_pull_resp)
        # _pull_resp += rxpkt['protocol'][4:12]
        _pull_resp += json.dumps(send).encode()
        write_log('Downlink:{} {}'.format(_pull_resp[:12].hex(), json.dumps(send).encode()))
        self.__tx_put(_pull_resp, time())

    def parse(self, data):
        if not data:
            return True
        if type(data) is not bytes:
            raise Exception('parse data must be bytes')
        _show_msg = 'GWID:{} VER:{} TOKEN:{} CMD:{}'.format(
            data[4:12].hex(), data[0], data[1:3].hex(), data[3]
        )
        _cmd = data[3]
        if _cmd == self.__cmd_push_data:
            write_log('{} push data'.format(_show_msg))
            self.__push_data(data)
            _push_ack = data[:3]
            _push_ack += self.__cmd_push_ack.to_bytes(length=1, byteorder='little')
            _push_ack += data[4:12]
            self.__tx_put(_push_ack)
        elif _cmd == self.__cmd_pull_data:
            write_log('{} pull data'.format(_show_msg))
            _pull_ack = data[:3]
            _pull_ack += self.__cmd_pull_ack.to_bytes(length=1, byteorder='little')
            _pull_ack += data[4:12]
            self.__tx_put(_pull_ack)
        elif _cmd == self.__cmd_tx_ack:
            write_log('{} tx ack'.format(_show_msg))


if __name__ == '__main__':
    pass
