
import json
import base64
import struct
import pandas as pd
from urllib import request
from time import time, sleep, mktime, strftime, strptime, localtime
from traceback import format_exc

log_name = ''


def write_log(_str):
    global log_name
    _data = strftime("%Y-%m-%d %H:%M:%S", localtime())
    if not log_name:
        log_name = strftime("log/%Y-%m-%d_%H%M%S.log", localtime())
    _data += '.%03d ' % (int(time() * 1000) % 1000)
    _data += _str
    try:
        print(_data)
        with open(log_name, 'a+') as f:
            f.write(_data + '\n')
            f.flush()
    except Exception as e:
        print('{}\n{}'.format(e, format_exc()))


class History(object):
    __uplink_url = 'https://qootone.iotsquare.xyz/api/device/history?'
    __downlink_url = 'https://qootone.iotsquare.xyz/api/device/downlink/history?'
    __token = 'B7d8iYYpF4xCwvisnGcRk4ktu5EgTRZkF96fwR8e58A='
    __headers = {
        # 'x-access-token': __token
        'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1Nzk0MTM1OTAsImlkIjozNSwidG9rZW4iOiI1MDY1NzE2YzQ0NjU1NDZmNTE1OTRlNGUifQ.e4t96LWVRGXR5BjhMs81v5Itza_MY3dN86AmrU5fnGI'
    }

    def __init__(self):
        # self.do_parse_uplink()
        # self.do_parse_downlink()
        self.do_parse_qootone('2020-1-17.xlsx')
        pass

    def do_parse_qootone(self, excel):
        deveui = pd.read_excel(excel)
        _not_data = []
        _not_update = []
        _new_data = {'deveui': [], 'temp': [], 'ap': [], 'bat': []}
        for eui in deveui.iloc[:, 1]:
            eui = eui.lower()
            _data = self.get_history(self.__uplink_url, eui, '2020-01-17 00:00:00', '2020-01-18 23:59:59', size=20)
            if _data[2] > 0:
                _data = _data[3][-1]['data']
                _data = base64.b64decode(_data.encode())
                if len(_data) in [6, 9, 12, 15]:
                    _temp = round(struct.unpack('h', _data[1:3])[0] / 100, 2)
                    _ap = struct.unpack('H', _data[3:5])[0]
                    _bat = round((_data[5] - 1)*100 / 253, 1)
                    _new_data['deveui'].append(eui)
                    _new_data['temp'].append(_temp)
                    _new_data['ap'].append(_ap)
                    _new_data['bat'].append(_bat)
                    print('deveui:{} temp:{} ap:{} bat:{}'.format(eui, _temp, _ap, _bat))
                else:
                    print('deveui:{} has not upgrade'.format(eui))
                    _not_update.append(eui)
            else:
                print('deveui:{} not data'.format(eui))
                _not_data.append(eui)
        pd.DataFrame({'deveui': _not_update}).to_excel('not_update.xlsx', index=False)
        pd.DataFrame({'deveui': _not_data}).to_excel('not_data.xlsx', index=False)
        pd.DataFrame(_new_data).to_excel('new_data.xlsx', index=False)

    def do_parse_uplink(self):
        _data = self.get_history(self.__uplink_url, '205137573236a61a', '2019-11-14 10:00:00', '2019-11-15 09:21:00')
        print('start={} stop={} count={}'.format(_data[0], _data[1], _data[2]))
        data_list = _data[3]
        _sf7bw125 = [True if _d['sfbw'] == 'SF7BW125' else False for _d in data_list]
        _sf8bw125 = [True if _d['sfbw'] == 'SF8BW125' else False for _d in data_list]
        _sf9bw125 = [True if _d['sfbw'] == 'SF9BW125' else False for _d in data_list]
        _sf10bw125 = [True if _d['sfbw'] == 'SF10BW125' else False for _d in data_list]
        _sf11bw125 = [True if _d['sfbw'] == 'SF11BW125' else False for _d in data_list]
        _sf12bw125 = [True if _d['sfbw'] == 'SF12BW125' else False for _d in data_list]
        _sf7bw125_time = []
        _sf8bw125_time = []
        _sf9bw125_time = []
        _sf10bw125_time = []
        _sf11bw125_time = []
        _sf12bw125_time = []
        for idx, data in enumerate(data_list):
            if _sf7bw125[idx]:
                _sf7bw125_time.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data['createtime']/1000))))
            if _sf8bw125[idx]:
                _sf8bw125_time.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data['createtime']/1000))))
            if _sf9bw125[idx]:
                _sf9bw125_time.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data['createtime']/1000))))
            if _sf10bw125[idx]:
                _sf10bw125_time.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data['createtime']/1000))))
            if _sf11bw125[idx]:
                _sf11bw125_time.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data['createtime']/1000))))
            if _sf12bw125[idx]:
                _sf12bw125_time.append(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data['createtime']/1000))))
        if not _sf7bw125_time:
            _sf7bw125_time.append('')
        if not _sf8bw125_time:
            _sf8bw125_time.append('')
        if not _sf9bw125_time:
            _sf9bw125_time.append('')
        if not _sf10bw125_time:
            _sf10bw125_time.append('')
        if not _sf11bw125_time:
            _sf11bw125_time.append('')
        if not _sf12bw125_time:
            _sf12bw125_time.append('')
        print('uplink={}'.format(len(data_list)))
        print('sf7bw125={} start={} stop={}'.format(sum(_sf7bw125), _sf7bw125_time[-1], _sf7bw125_time[0]))
        print('sf8bw125={} start={} stop={}'.format(sum(_sf8bw125), _sf8bw125_time[-1], _sf8bw125_time[0]))
        print('sf9bw125={} start={} stop={}'.format(sum(_sf9bw125), _sf9bw125_time[-1], _sf9bw125_time[0]))
        print('sf10bw125={} start={} stop={}'.format(sum(_sf10bw125), _sf10bw125_time[-1], _sf10bw125_time[0]))
        print('sf11bw125={} start={} stop={}'.format(sum(_sf11bw125), _sf11bw125_time[-1], _sf11bw125_time[0]))
        print('sf12bw125={} start={} stop={}'.format(sum(_sf12bw125), _sf12bw125_time[-1], _sf12bw125_time[0]))
        print('start:{}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data_list[-1]['createtime']/1000)))))
        print('last:{}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime(int(data_list[0]['createtime']/1000)))))
        print('first:{}'.format(data_list[-1]))
        print('last:{}'.format(data_list[0]))

    def do_parse_downlink(self):
        _data = self.get_history(self.__downlink_url, '205137573236a61a', '2019-11-14 10:00:00', '2019-11-15 09:21:00')
        print('start={} stop={} count={}'.format(_data[0], _data[1], _data[2]))
        _data = _data[3]
        sent = 0
        _first = ''
        _last = ''
        print(_data[0])
        for _d in _data:
            # print(_d)
            if _d['sent']:
                if not _first:
                    _last = _d['dltime']
                _first = _d['dltime']
                sent += 1
        print('send={}'.format(sent))
        _first = int(_first/1000)
        _last = int(_last/1000)
        print('start:{} stop:{}'.format(
            strftime("%Y-%m-%d %H:%M:%S", localtime(_first)),
            strftime("%Y-%m-%d %H:%M:%S", localtime(_last)))
        )

    def get_history(self, url, eui, start, stop, page=1, size=100000):
        start_ts = int(mktime(strptime(start, "%Y-%m-%d %H:%M:%S")))
        stop_ts = int(mktime(strptime(stop, "%Y-%m-%d %H:%M:%S")))
        _url = url + 'devEUI={}&pageNo={}&pageSize={}&startTime={}&endTime={}'.format(
            eui, page, size, start_ts, stop_ts
        )
        _request = request.Request(_url, headers=self.__headers)
        try:
            _respond = request.urlopen(_request, timeout=3)
            _context = _respond.read().decode('utf-8')
            _data_dict = json.loads(_context)
            if _data_dict['msg'].upper() == 'OK':
                return start, stop, _data_dict['amount'], _data_dict['data']
        except Exception as e:
            _ = e
        return False


if __name__ == '__main__':
    his = History()
