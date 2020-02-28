
import os
import re
import json
import queue
import socket
import sqlite3
import threading
from time import time, sleep, strftime, localtime
from traceback import format_exc

import xlwt
import xlrd
import serial
from serial.tools import list_ports

import requests


def write_log(_data):
    _time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    _micro_sec = '{}'.format(int(time() * 1000 % 1000)).rjust(3, '0')
    _data = '{}.{} {}'.format(_time, _micro_sec, _data)
    try:
        print(_data)
        with open('log.txt', 'a+') as f:
            f.write(_data + '\n')
    except Exception as e:
        print('LOG except:{}\n{}'.format(e, format_exc()))


class Time(object):
    __url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'

    def time(self):
        try:
            _req = requests.get(self.__url, timeout=1)
            _respond = json.loads(_req.content.decode())
            _ts = _respond['data']['t']
            _ts = int(_ts) / 1000
        except:
            _ts = time()
        return _ts


class File(object):
    @staticmethod
    def exists(file):
        try:
            return os.path.exists(file)
        except Exception as e:
            write_log('File except:{}\n{}'.format(e, format_exc()))
        return False

    @staticmethod
    def create(file):
        try:
            f = open(file, 'w')
            f.close()
            return True
        except Exception as e:
            write_log('File except:{}\n{}'.format(e, format_exc()))
        return False

    @staticmethod
    def delete(file):
        try:
            if os.path.exists(file) is True:
                os.remove(file)
            return True
        except Exception as e:
            write_log('File except:{}\n{}'.format(e, format_exc()))
        return False

    @staticmethod
    def size(file):
        return os.path.getsize(file)

    def read(self, file, mode='r'):
        if not self.exists(file):
            return False
        with open(file, mode) as f:
            return f.read()

    def write(self, file, data, mode='w'):
        if not self.create(file):
            return False
        with open(file, mode) as f:
            f.write(data)
        return True

    def copy(self, src, des):
        if not self.exists(src):
            return False
        if not self.create(des):
            return False
        with open(src, 'rb') as fr:
            fw = open(des, 'wb')
            while True:
                data = fr.read(1000)
                if not data:
                    break
                fw.write(data)
            fw.close()

    def move(self, src, des):
        if not self.copy(src, des):
            return False
        return self.delete(src)


class Serial(object):
    __byte = 8
    __parity = serial.PARITY_NONE
    __stop = 1
    __port = serial.Serial()
    __queue_max = 50
    __name = ''

    def __init__(self, desc, baud, timeout=100, wakeup=False):
        self.__desc = desc
        self.__baud = baud
        self.__tout = timeout/1000
        self.__wakeup = wakeup
        self.__queue = queue.Queue()
        self.__tx_buffer = ''

        self.__thread_evt = threading.Thread(target=self.__on_serial_thread)
        self.__thread_evt.setDaemon(True)
        self.__thread_evt.start()

    @staticmethod
    def get_port_to_list():
        _list = []
        for comport in list_ports.comports():
            name = str(comport)
            name = name.split(' ')[0]
            _list.append(name)
        return _list

    @staticmethod
    def get_port_by_hid(hid):
        for comport in list_ports.comports():
            if hid in comport.hwid:
                name = str(comport)
                name = name.split(' ')[0]
                return name
        return None

    def get_port_name(self):
        return self.__port.name

    def get_port_open(self):
        return self.__port.is_open
    
    def get(self):
        if self.__queue.empty():
            return ''
        return self.__queue.get()

    def open(self):
        if 'COM' in self.__desc:
            port = self.__desc
        else:
            port = self.get_port_by_hid(self.__desc)
        try:
            self.__port = serial.Serial(
                port=port,
                baudrate=self.__baud,
                bytesize=self.__byte,
                stopbits=self.__stop,
                parity=self.__parity,
                timeout=0)
            write_log('open pass:{}'.format(port))
            return True
        except Exception as e:
            _ = e
            # write_log('open fail:{}\n{}'.format(e, format_exc()))
        return False

    def close(self):
        name = self.__port.name
        try:
            self.__port.close()
            write_log('close pass:{}'.format(name))
            return True
        except Exception as e:
            write_log('close fail:{}\n{}'.format(e, format_exc()))
        return False

    def open_rst(self):
        self.close()
        return self.open()

    def send(self, data, directory=False):
        if not data:
            return True
        data = data.strip() + '\r\n'
        name = self.__port.name
        try:
            if directory:
                if self.__wakeup:
                    self.__port.write(b'\xff\xff\xff\xff')
                self.__port.write(data.encode('utf-8'))
                write_log('{} send:{}'.format(name, data))
            else:
                self.__tx_buffer = data
            return True
        except Exception as e:
            write_log('{} send except:{}\n{}'.format(name, e, format_exc()))
            self.close()
        return False

    def read(self):
        name = self.__port.name
        data = ''
        start = time()
        try:
            while (time() - start) <= self.__tout:
                rx_byte = self.__port.read()
                if not rx_byte:
                    break
                if rx_byte == b'\n':
                    break
                data += rx_byte.decode("utf-8", "ignore")
                start = time()
                sleep(0.002)
            data = data.strip()
            if data:
                write_log('{} read:{}'.format(name, data))
        except Exception as e:
            write_log('{} read except:{}\n{}'.format(name, e, format_exc()))
            self.close()
        return data

    def send_wait_regular(self, tx, regular=r'.+', tout=None):
        if tout:
            tout = tout/1000
        else:
            tout = self.__tout
        self.send(tx, True)
        start = time()
        while time() - start <= tout:
            rx = self.get()
            if rx:
                start = time()
            if re.match(regular, rx):
                return rx
            sleep(0.005)
        return False

    def __on_serial_thread(self):
        while True:
            sleep(0.01)
            if not self.__port.is_open:
                self.open()
                continue
            if self.__tx_buffer:
                self.send(self.__tx_buffer, True)
                self.__tx_buffer = ''
            line = self.read()
            if not line:
                continue
            self.__queue.put(line)
            while self.__queue.qsize() >= self.__queue_max:
                self.__queue.get()


class SQLite3(object):
    def __init__(self, database):
        self.__conn = sqlite3.connect(database, check_same_thread=False)

    def execute(self, content):
        try:
            if content.find('SELECT') == 0:
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

    def create(self, table_name, table_item, item_data):
        content = '{} {} {} {}'.format('CREATE', table_name, table_item, item_data)
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

    def select(self, table_name, table_item, data_limit=''):
        content = '{} {} FROM {}'.format('SELECT', table_item, table_name)
        if data_limit:
            content += ' WHERE %s' % data_limit
        return self.execute(content)


class Socket(object):
    __local_addr = None
    __remote_addr = None

    __sock_udp = None
    __sock_tcp = None
    __sock_client = None

    __sock_open = False

    def __init__(self, timeout=50):
        self.__tout = timeout / 1000
        self.__local_ip = self.get_local_ip()
        self.__remote_ip = self.__local_ip

    def timeout(self, tout=None):
        if not tout:
            return self.__tout * 1000
        self.__tout = tout / 1000
        if self.__sock_udp:
            self.__sock_udp.settimeout(self.__tout)
        if self.__sock_tcp:
            self.__sock_tcp.settimeout(self.__tout)
        if self.__sock_client:
            self.__sock_client.settimeout(self.__tout)
        return self.__tout * 1000

    @staticmethod
    def get_local_ip():
        ip_str = '127.0.0.1'
        for addr in socket.getaddrinfo(socket.gethostname(), None):
            if str(addr[0]) == 'AddressFamily.AF_INET':
                ip = str(addr[4][0])
                ip = [int(x) for x in ip.split('.')]
                if 1 < ip[3] < 255:
                    ip_str = '{}.{}.{}.{}'.format(ip[0], ip[1], ip[2], ip[3])
                    break
        write_log('get_local_ip:{}'.format(ip_str))
        return ip_str

    def is_open(self):
        return self.__sock_open

    def udp_new(self, local_port, remote_port=8888):
        self.__local_addr = (self.__local_ip, local_port)
        self.__remote_addr = ('<broadcast>', remote_port)
        try:
            self.__sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__sock_udp.bind(self.__local_addr)
            self.__sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.__sock_udp.settimeout(self.__tout)
            self.__sock_open = True
            write_log('udp_new:{}'.format(self.__local_addr))
            return True
        except Exception as e:
            self.__sock_open = False
            write_log('udp_new except:{}\n{}'.format(e, format_exc()))
        return False

    def udp_send(self, data, remote=None):
        if not data:
            return True
        if not remote:
            remote = self.__remote_addr
        try:
            data = data.encode('utf-8', 'ignore')
            assert isinstance(self.__sock_udp, socket.socket)
            self.__sock_udp.sendto(data, remote)
            write_log('udp_send:{}'.format(data))
            return True
        except Exception as e:
            self.__sock_open = False
            write_log('udp_send except:{}\n{}'.format(e, format_exc()))
        return False

    def udp_recv(self, redirect=True):
        data = None
        try:
            assert isinstance(self.__sock_udp, socket.socket)
            data, addr = self.__sock_udp.recvfrom(2000)
            if addr and redirect:
                self.__remote_addr = addr
            if data:
                data = data.decode('utf-8', 'ignore')
                write_log('udp_recv:{}'.format(data))
        except Exception as e:
            if str(e) == 'timed out':
                pass
            else:
                self.__sock_open = False
                write_log('udp_recv except:{}\n{}'.format(e, format_exc()))
        return data

    def udp_send_wait_regular(self, tx, regular='.*'):
        if not self.udp_send(tx):
            return False
        _start = _now = time()
        while _now - _start < self.__tout:
            line = self.udp_recv()
            if line and re.match(regular, line):
                return line.strip()
            sleep(0.01)
        return False

    def tcp_new_server(self, port, num=1):
        self.__local_addr = (self.__local_ip, int(port))
        try:
            self.__sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock_tcp.bind(self.__local_addr)
            self.__sock_tcp.listen(int(num))
            self.__sock_tcp.settimeout(self.__tout)
            self.__sock_open = True
            write_log('tcp_new_server:{}'.format(self.__local_addr))
            return True
        except Exception as e:
            self.__sock_open = False
            write_log('tcp_new_server except:{}\n{}'.format(e, format_exc()))
        return False

    def tcp_new_client(self, ip, port):
        self.__remote_addr = (str(ip), int(port))
        try:
            self.__sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock_client.connect(self.__remote_addr)
            self.__sock_client.settimeout(self.__tout)
            self.__sock_open = True
            write_log('tcp_new_client:{}'.format(self.__remote_addr))
            return True
        except Exception as e:
            self.__sock_open = False
            write_log('tcp_new_client except:{}\n{}'.format(e, format_exc()))
        return False

    def tcp_accept(self):
        try:
            assert isinstance(self.__sock_tcp, socket.socket)
            client, addr = self.__sock_tcp.accept()
            if addr and client:
                self.__remote_addr = addr
                self.__sock_client = client
                self.__sock_client.settimeout(self.__tout)
                write_log('tcp_accept:{}'.format(self.__remote_addr))
                return True
        except Exception as e:
            if str(e) == 'timed out':
                pass
            else:
                write_log('tcp_accept except:{}\n{}'.format(e, format_exc()))
        return False

    def tcp_recv(self):
        data = None
        try:
            assert isinstance(self.__sock_client, socket.socket)
            data = self.__sock_client.recv(2000)
            if data:
                data = data.decode('utf-8', 'ignore')
                write_log('tcp_recv:{}'.format(data))
        except Exception as e:
            if str(e) == 'timed out':
                pass
            else:
                self.__sock_open = False
                write_log('tcp_recv except:{}\n{}'.format(e, format_exc()))
        return data

    def tcp_send(self, data):
        if not data:
            return True
        try:
            assert isinstance(self.__sock_client, socket.socket)
            data = data.encode('utf-8', 'ignore')
            self.__sock_client.send(data)
            write_log('tcp_send:{}'.format(data))
            return True
        except Exception as e:
            self.__sock_open = False
            write_log('tcp_send except:{}\n{}'.format(e, format_exc()))
        return False


class Excel(object):
    def write(self, file, head, lines):
        filename, suffix = os.path.splitext(file)
        if suffix == '.xls':
            return self.__write_xlwt(file, head, lines)
        return File

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


class QtColor(object):
    white = 'color: rgb(255, 255, 255);'
    black = 'color: rgb(0, 0, 0);'
    red = 'color: rgb(170, 0, 0);'
    green = 'color: rgb(0, 170, 0);'
    blue = 'color: rgb(85, 0, 255);'


class  Test(object):
    @staticmethod
    def serial_thread():
        ss = Serial('COM9', 115200, 500)
        send_ts = time()
        while True:
            if time() - send_ts >= 1:
                ss.send('AT')
            ss.get()

    @staticmethod
    def serial_wait():
        ss = Serial('COM9', 115200, 500)
        send_ts = time()
        while True:
            if time() - send_ts >= 1:
                ss.send_wait_regular('AT', r'\+AT: OK')

    @staticmethod
    def udp(local_port, remote_port):
        ss = Socket()
        ss.udp_new(local_port, remote_port)
        send_ts = time()
        while True:
            if time() - send_ts >= 1:
                send_ts = time()
                ss.udp_send('udp one send test\n')
            ss.udp_recv()
            if not ss.is_open():
                break

    @staticmethod
    def tcp_client(remote_ip, remote_port):
        ss = Socket()
        if not remote_ip:
            remote_ip = ss.get_local_ip()
        ss.tcp_new_client(remote_ip, remote_port)
        send_ts = time()
        while True:
            if time() - send_ts >= 1:
                send_ts = time()
                ss.tcp_send('tcp one send test\n')
            ss.tcp_recv()
            if not ss.is_open():
                break

    @staticmethod
    def tcp_server(local_port):
        ss = Socket()
        ss.tcp_new_server(local_port)
        while not ss.tcp_accept():
            sleep(0.1)
        send_ts = time()
        while True:
            if time() - send_ts >= 1:
                send_ts = time()
                ss.tcp_send('tcp one send test\n')
            ss.tcp_recv()
            if not ss.is_open():
                break

    @staticmethod
    def file_copy():
        f = File()
        f.copy('log.txt', 'copy.txt')


if __name__ == '__main__':
    test = Test()
    t = Time()
    print(t.time())
    print(time())
    # test.serial_thread()
    # test.serial_wait()
    # test.udp(123, 777)
    # test.tcp_client(None, 888)
    # test.tcp_server(999)
    # test.file_copy()
