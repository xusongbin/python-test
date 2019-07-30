#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import paramiko

import logging
import traceback
from md_logging import setup_log

setup_log()
write_log = logging.getLogger('ssh')


class Ssh(object):
    def __init__(self, ip, port, username, password, timeout=1):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        write_log.debug('IP:{} Port:{} Username:{} Password:{} Timeout:{}'.format(
            self.ip, self.port, self.username, self.password, self.timeout
        ))

    def connect(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(self.ip, self.port, self.username, self.password, timeout=self.timeout)
            paramiko.SFTPClient.from_transport(ssh_client.get_transport())
            write_log.debug('connect successful!')
            return ssh_client
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        return None

    def exec_command(self, cmd):
        ssh_client = self.connect()
        if not ssh_client:
            return None
        data = None
        try:
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            data = str(stdout.read().decode('utf-8', 'ignore'))
            write_log.debug('exec_command:{}'.format(cmd))
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        ssh_client.close()
        return data

    def transport_file(self, local, remote, method='put'):
        # method:'put' send local file to remote
        # method:'get' download remote file to local
        ssh_client = self.connect()
        if not ssh_client:
            return False
        status = False
        try:
            sftp = ssh_client.open_sftp()
            assert isinstance(sftp, paramiko.SFTPClient)
            if method == 'put':
                sftp.put(local, remote)
            elif method == 'get':
                sftp.get(remote, local)
            status = True
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        ssh_client.close()
        return status

    def on_put_directory(self, sftp, local, remote):
        if os.path.isdir(local):
            try:
                sftp.mkdir(remote)
            except:
                pass
            path_remote = remote
            for root, dirs, files in os.walk(local):
                path_inc = root[len(local):]
                path_local = root
                try:
                    for d in dirs:
                        sftp.mkdir(os.path.join(path_remote + path_inc, d).replace('\\', '/'))
                    for file in files:
                        sftp.put(
                            os.path.join(path_local, file).replace('\\', '/'),
                            os.path.join(path_remote + path_inc, file).replace('\\', '/')
                        )
                except:
                    print('some except!')
        else:
            file_local = local
            if os.path.isdir(remote) or not remote:
                file_remote = os.path.basename(file_local)
            else:
                file_remote = remote
            try:
                sftp.put(file_local, file_remote)
                return True
            except:
                pass
        return False

    def on_get_directory(self, sftp, local, remote):
        if not os.path.exists(local):
            os.mkdir(local)
        for file in sftp.listdir(remote):
            path_local = os.path.join(local, file).replace('\\', '/')
            path_remote = os.path.join(remote, file).replace('\\', '/')
            if file.find('.') == -1:
                if not os.path.exists(path_local):
                    os.mkdir(path_local)
                self.on_get_directory(sftp, path_local, path_remote)
            else:
                sftp.get(path_remote, path_local)

    def transport_directory(self, local, remote, method='put'):
        # method:'put' send a directory to remote
        # method:'get' download a directory
        ssh_client = self.connect()
        if not ssh_client:
            return False
        status = False
        try:
            sftp = ssh_client.open_sftp()
            assert isinstance(sftp, paramiko.SFTPClient)
            if method == 'put':
                self.on_put_directory(sftp, local, remote)
            elif method == 'get':
                self.on_get_directory(sftp, local, remote)
            status = True
        except Exception as e:
            write_log.error('{}\n{}'.format(e, traceback.format_exc()))
        ssh_client.close()
        return status

    def exec_listdir(self, path=''):
        listdir = []
        recv = self.exec_command('ls -l {}'.format(path))
        if not recv:
            return listdir
        for line in recv.split('\n'):
            line = line.strip()
            if not re.match(
                    r'd.*[ ]+[A-Za-z0-9]+[ ]+[A-Za-z0-9]+[ ]+\d+[ ]+[A-Za-z]+[ ]+\d+[ ]+\d\d:\d\d[ ]+.*',
                    line
            ):
                continue
            _list = line.split(' ')
            _list = [x for x in _list if x != '']
            listdir.append(_list[-1])
        return listdir

    def exec_listfile(self, path=''):
        listfile = []
        recv = self.exec_command('ls -l {}'.format(path))
        if not recv:
            return listfile
        for line in recv.split('\n'):
            line = line.strip()
            if not re.match(
                    r'-.*[ ]+[A-Za-z0-9]+[ ]+[A-Za-z0-9]+[ ]+\d+[ ]+[A-Za-z ]+[ ]+\d+[ ]+\d\d:\d\d[ ]+.*\.zip',
                    line
            ):
                continue
            _list = line.split(' ')
            _list = [x for x in _list if x != '']
            listfile.append(_list)
        return listfile


if __name__ == '__main__':
    test_ssh = Ssh('120.79.88.165', 28923, 'songbin', 'VJtYbYvYrx7g')
    # print(test_ssh.exec_listdir())
    test_ssh.transport_directory('1', '1', method='get')
