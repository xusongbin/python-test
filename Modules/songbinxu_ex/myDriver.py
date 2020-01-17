
import os
import re
import queue
import struct
import socket
import sqlite3
import threading
from time import time, sleep, strftime, localtime
from traceback import format_exc

import xlwt
import xlrd
import serial
from serial.tools import list_ports
from Crypto.Cipher import AES

from myXmodem import XMODEM


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

    @staticmethod
    def aes_encrypt(fin, fout, key=b'RisingHF20150203'):
        cryptos = AES.new(key, AES.MODE_ECB)
        with open(fin, 'rb') as rf:
            data = rf.read()
            add = len(data) % 16
            if add:
                data += b'\x00' * (16 - add)
            with open(fout, 'wb') as wf:
                wf.write(cryptos.encrypt(data))

    @staticmethod
    def aes_decrypt(fin, fout, key=b'RisingHF20150203'):
        cryptos = AES.new(key, AES.MODE_ECB)
        with open(fin, 'rb') as rf:
            with open(fout, 'wb') as wf:
                wf.write(cryptos.decrypt(rf.read()))


class Serial(object):
    __len = 8
    __parity = serial.PARITY_NONE
    __stop = 1
    __port = serial.Serial()
    __queue_max = 500
    __name = ''
    __byte = False

    def __init__(self, desc, baud, timeout=300, wakeup=False, byte=False):
        self.__desc = desc
        self.__baud = baud
        self.__tout = timeout/1000
        self.__wakeup = wakeup
        self.__byte = byte
        self.__queue = queue.Queue()
        self.__tx_buffer = ''
        self.__xmodem = XMODEM(self.__get_char, self.__put_char, mode='xmodem1k')
        self.__xmodem_sta = False
        self.close()

        self.__thread_evt = threading.Thread(target=self.__on_serial_thread)
        self.__thread_evt.setDaemon(True)
        self.__thread_evt.start()

    def xmodem_send(self, path):
        self.__xmodem_sta = True
        try:
            with open(path, 'rb') as f:
                result = self.__xmodem.send(f, timeout=5000, retry=1000)
        except Exception as e:
            write_log('xmodem send fail:{}\n{}'.format(e, format_exc()))
            result = False
        self.__xmodem_sta = False
        return result

    def xmodem_recv(self, path):
        self.__xmodem_sta = True
        try:
            with open(path, 'wb') as f:
                result = self.__xmodem.recv(f)
            return result
        except Exception as e:
            write_log('xmodem recv fail:{}\n{}'.format(e, format_exc()))
            result = False
        self.__xmodem_sta = False
        return result

    def xmodem_step(self):
        return self.__xmodem.step

    def __get_char(self, size, timeout=0.001):
        _data = None
        _now = time()
        while (time() - _now) < timeout:
            _data = self.__port.read(size) or None
            if _data:
                return _data
            else:
                sleep(0.001)
            _now = time()
        return _data

    def __put_char(self, data):
        sleep(0.005)
        return self.__port.write(data)

    @staticmethod
    def get_port_to_list():
        _list = []
        try:
            for comport in list_ports.comports():
                name = str(comport)
                name = name.split(' ')[0]
                _list.append(name)
        except Exception as e:
            _ = e
        return _list

    @staticmethod
    def get_port_by_hid(hid):
        try:
            for comport in list_ports.comports():
                if hid in comport.hwid:
                    name = str(comport)
                    name = name.split(' ')[0]
                    return name
        except Exception as e:
            _ = e
        return None

    def reset_describe(self, desc):
        self.__desc = desc
        self.open_rst()

    def reset_rate(self, rate):
        self.__baud = rate
        self.open_rst()

    def get_port_name(self):
        try:
            return self.__port.name
        except Exception as e:
            _ = e
            return None

    def get_port_open(self):
        try:
            return self.__port.is_open
        except Exception as e:
            _ = e
            return False
    
    def get(self):
        if self.__queue.empty():
            return ''
        if self.__byte:
            return self.__queue.get()
        else:
            return self.__queue.get().decode('utf-8', 'ignore').strip()

    def open(self):
        if 'COM' in self.__desc:
            port = self.__desc
        else:
            port = self.get_port_by_hid(self.__desc)
        if not port:
            return False
        try:
            self.__port = serial.Serial(
                port=port,
                baudrate=self.__baud,
                bytesize=self.__len,
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
        name = self.__port.name
        try:
            if directory:
                if self.__wakeup:
                    self.__port.write(b'\xff\xff\xff\xff')
                if type(data) is str:
                    data = data.strip() + '\r\n'
                    self.__port.write(data.encode('utf-8'))
                else:
                    self.__port.write(data)
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
        data = b''
        start = time()
        try:
            while (time() - start) <= self.__tout:
                sleep(0.002)
                rx_byte = self.__port.read()
                if not rx_byte:
                    continue
                if not self.__byte and rx_byte == b'\n':
                    break
                data += rx_byte
                start = time()
            if data:
                write_log('{} read:{}'.format(name, data))
        except Exception as e:
            write_log('{} read except:{}\n{}'.format(name, e, format_exc()))
            self.close()
        return data

    def send_wait_regular(self, tx, regular=None, tout=None):
        if tout:
            tout = tout/1000
        else:
            tout = self.__tout
        self.send(tx)
        start = time()
        while (time() - start) <= tout:
            rx = self.get()
            if rx:
                start = time()
                if self.__byte or not regular:
                    return rx
                elif re.match(regular, rx):
                    return rx
            sleep(0.005)
        return False

    def recv_wait_send(self, tx, regular=r'.+', tout=None):
        if tout:
            tout = tout/1000
        else:
            tout = self.__tout
        start = time()
        while (time() - start) <= tout:
            rx = self.get()
            if rx:
                start = time()
                if self.__byte:
                    return rx
                elif re.match(regular, rx):
                    return rx
            sleep(0.005)
        self.send(tx)
        return False

    def __on_serial_thread(self):
        while True:
            sleep(0.01)
            if self.__xmodem_sta:
                continue
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


class UdpSocket(object):
    __sock_udp = None
    __sock_open = False
    __queue = queue.Queue()

    def __init__(self, local_port, timeout=50, log=True):
        self.__local_addr = (self.get_local_ip(), local_port)
        self.__remote_addr = None
        self.__tout = timeout / 1000
        self.__log = log

        self.__thread_evt = threading.Thread(target=self.__on_socket_thread)
        self.__thread_evt.setDaemon(True)
        self.__thread_evt.start()

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

    def get(self):
        if not self.__queue.empty():
            self.__remote_addr, data = self.__queue.get()
            return data
        return None

    def open(self):
        try:
            self.__sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__sock_udp.bind(self.__local_addr)
            self.__sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.__sock_udp.settimeout(self.__tout)
            self.__sock_open = True
            write_log('UDP open:{}'.format(self.__local_addr))
            return True
        except Exception as e:
            write_log('UDP open:{}\n{}'.format(e, format_exc()))
        self.__sock_open = False
        return False

    def close(self):
        self.__sock_open = False
        try:
            self.__sock_udp.close()
        except Exception as e:
            write_log('UDP close:{}\n{}'.format(e, format_exc()))

    def send(self, data, remote=None):
        if not data:
            return True
        if not remote:
            remote = self.__remote_addr
        try:
            if type(data) is str:
                data = data.encode('utf-8', 'ignore')
            assert isinstance(self.__sock_udp, socket.socket)
            self.__sock_udp.sendto(data, remote)
            if self.__log:
                write_log('UDP send {}:{}'.format(remote, data))
            return True
        except Exception as e:
            self.__sock_open = False
            write_log('udp_send except:{}\n{}'.format(e, format_exc()))
        return False

    def recv(self):
        try:
            assert isinstance(self.__sock_udp, socket.socket)
            data, addr = self.__sock_udp.recvfrom(2000)
            if data:
                if self.__log:
                    write_log('UDP recv {}:{}'.format(addr, data))
                self.__remote_addr = addr
                return addr, data
        except Exception as e:
            if str(e) == 'timed out':
                pass
            else:
                self.__sock_open = False
                write_log('UDP recv:{}\n{}'.format(e, format_exc()))
        return None

    def udp_send_wait_regular(self, tx, regular='.*'):
        self.send(tx)
        _start = time()
        while (time() - _start) < self.__tout:
            line = self.get()
            if line and re.match(regular, line):
                return line
            sleep(0.01)
        return False

    def __on_socket_thread(self):
        while True:
            sleep(0.001)
            if not self.__sock_open:
                self.close()
                self.open()
                continue
            data = self.recv()
            if data:
                self.__queue.put(data)


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
    bg_white = 'background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);'
    bg_black = 'background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);'
    bg_red = 'background-color: rgb(170, 0, 0);color: rgb(0, 0, 0);'
    bg_green = 'background-color: rgb(0, 170, 0);color: rgb(0, 0, 0);'
    bg_blue = 'background-color: rgb(85, 0, 255);color: rgb(0, 0, 0);'


class Test(object):
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
    LAP_CMD_DELAY = 0x9C
    LAP_CMD_SDELAY = 0x9C
    LAP_CMD_ULPRD = 0x9D
    LAP_CMD_SULPRD = 0x9D
    LAP_CMD_DLSQ = 0x9E
    LAP_CMD_DINFO = 0x9F
    LAP_CMD_FDEFAULT = 0xA0
    LAP_CMD_USIGNAL = 0xA1
    LAP_CMD_TEST = 0xFE
    LAP_CMD_CUSTOM = 0xFF

    def __init__(self):
        self.device = {}
        # dd = '9F13323153464530059004012410070A1262001410000C00C100'
        # print(bytes.fromhex(dd))
        # self.parse(bytes.fromhex(dd))
        # print(self.device)

    def parse(self, data):
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
        self.device['acc'] = [int(x / 16) for x in struct.unpack('>hhh', data)]
        self.device['acc_g'] = 0
        self.device['acc_g'] += pow(self.device['acc'][0], 2)
        self.device['acc_g'] += pow(self.device['acc'][1], 2)
        self.device['acc_g'] += pow(self.device['acc'][2], 2)
        self.device['acc_g'] = int(self.device['acc_g'] ** 0.5)


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

    @staticmethod
    def hex_to_dec(data):
        if not re.match(r'(0[xX])?[0-9A-Fa-f]+', data):
            raise Exception('input is not hex')
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
        if len(data) != 4:
            raise Exception('input bytes length is not 4')
        fmt = '<'
        if order == 'big':
            fmt = '>'
        if sign:
            fmt += 'i'
        else:
            fmt += 'I'
        return struct.unpack('{}'.format(fmt), bytes(data))[0]

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
        if not re.match(r'[0-9A-Fa-f]+', data):
            raise Exception('input is not string')
        return bytes.fromhex(data)


if __name__ == '__main__':
    test = Test()
    tf = Transform()
    # print(tf.byte_to_longlong(b'\x00\x00\x00\x00\x00\x00\x00\x80', order='little', sign=False))
    # print(tf.byte_to_bool(b'\x02'))
    # print(tf.byte_to_float(b'\x00\x00\x00\x01'))
    print(tf.short_to_bytes(154))
    # print(tf.dec_to_sign_dec(0xFF))
    # print(hex(tf.sign_dec_to_dec(-1)))
    # print(tf.bytes_to_hex(b'\x00\x02'))
    # test.serial_thread()
    # test.serial_wait()
    # test.udp(123, 777)
    # test.tcp_client(None, 888)
    # test.tcp_server(999)
    # test.file_copy()
