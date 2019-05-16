
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


def run_udp_server(ip, port):
    udp_addr = (str(ip), int(port))
    udp_socket = socket(AF_INET, SOCK_DGRAM)  # UDP
    udp_socket.bind(udp_addr)
    while True:
        data, s_addr = udp_socket.recvfrom(1000)
        print('receive from %s:%s' % (str(s_addr), data.decode('utf-8', 'ignore')))
        udp_socket.sendto(data, s_addr)


def run_udp_clent(ip, port):
    udp_addr = (str(ip), int(port))
    udp_socket = socket(AF_INET, SOCK_DGRAM)  # UDP
    while True:
        udp_socket.sendto(b'test', udp_addr)
        sleep(1)


def run_tcp_server(ip, port):
    tcp_addr = (str(ip), int(port))
    tcp_socket = socket(AF_INET, SOCK_STREAM)  # TCP
    tcp_socket.bind(tcp_addr)
    tcp_socket.listen(1)
    while True:
        s_client, s_addr = tcp_socket.accept()
        print('connect %s' % str(s_addr))
        while True:
            data = s_client.recv(1000)
            if not data:
                break
            print('receive from %s:%s' % (str(s_addr), data.decode('utf-8', 'ignore')))
            s_client.send(data)
        s_client.close()


def run_tcp_clent(ip, port):
    tcp_addr = (str(ip), int(port))
    while True:
        try:
            tcp_socket = socket(AF_INET, SOCK_STREAM)  # TCP
            tcp_socket.connect(tcp_addr)
            while True:
                try:
                    tcp_socket.send(b'test')
                except Exception as e:
                    print('send:%s' % e)
                    break
                sleep(1)
            tcp_socket.close()
        except Exception as e:
            print('connect:%s' % e)
        sleep(1)


if __name__ == '__main__':
    # run_udp_server('127.0.0.1', 9999)
    # run_udp_clent('127.0.0.1', 777)
    # run_tcp_server('127.0.0.1', 9999)
    run_tcp_clent('127.0.0.1', 777)
