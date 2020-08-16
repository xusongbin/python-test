#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import queue
import socket
import threading
from traceback import format_exc
from time import time, sleep

from myDriver.hhLog import write_log


class UdpSocket(object):
    __sock_udp = None
    __sock_open = False
    __queue_rx = queue.Queue()
    __queue_tx = queue.Queue()

    def __init__(self, local_port, timeout=50, byte=False, log=True):
        self.__local_addr = (self.get_local_ip(), local_port)
        self.__remote_addr = None
        self.__tout = timeout / 1000
        self.__byte = byte
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

    def get(self, timeout=None):
        if not timeout:
            if self.__queue_rx.empty():
                return ''
            try:
                self.__remote_addr, data = self.__queue_rx.get()
            except Exception as e:
                _ = e
                return ''
            if self.__byte:
                return data
            else:
                return data.decode('utf-8', 'ignore').strip()
        _start = time()
        while (time() - _start) < timeout / 1000:
            sleep(0.005)
            if self.__queue_rx.empty():
                continue
            try:
                self.__remote_addr, data = self.__queue_rx.get()
            except Exception as e:
                _ = e
                return ''
            if self.__byte:
                return data
            else:
                return data.decode('utf-8', 'ignore').strip()
        return ''

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
        if not self.__sock_udp:
            return True
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
            assert isinstance(self.__sock_udp, socket.socket)
            if type(data) is str:
                self.__sock_udp.sendto(data.encode('utf-8', 'ignore'), remote)
            else:
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

    def send_wait_regular(self, tx, regular='.*'):
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
            if not self.__sock_open:
                sleep(0.1)
                self.close()
                self.open()
                continue
            data = self.recv()
            if not data:
                sleep(0.001)
            self.__queue_rx.put(data)


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
        _start = time()
        while (time() - _start) < self.__tout:
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


if __name__ == '__main__':
    udp = UdpSocket(5555)
    udp.get(3000)
