#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import winreg
import win32con
import win32api
from wmi import WMI


class Computer(object):
    __reg_dir = r'Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache'
    __reg_env = r'Environment'

    @staticmethod
    def cpu_id():
        _list = []
        for cpu in WMI().Win32_Processor():
            _list.append(cpu.ProcessorId.strip())
        return _list

    def get_install_dir(self, exe=None, value=None):
        if not exe and not value:
            return None
        if exe and '.exe' not in exe:
            exe = '{}.exe'.format(exe)
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.__reg_dir)
            _num = int(winreg.QueryInfoKey(key)[1])
        except Exception as e:
            _ = e
            return None
        _install = None
        for i in range(_num):
            try:
                path, name, _ = winreg.EnumValue(key, i)
                _basename = os.path.basename(path)
                if exe and exe.lower() == _basename.lower():
                    _install = os.path.split(path)[0]
                    break
                if value and value.lower() in name.lower():
                    _install = os.path.split(path)[0]
                    break
            except Exception as e:
                _ = e
        try:
            winreg.CloseKey(key)
        except Exception as e:
            _ = e
        return _install

    @staticmethod
    def env_get(name):
        return os.getenv(name)

    def env_set(self, name, value):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.__reg_env, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
            winreg.CloseKey(key)
            # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, self.__reg_env)
        except Exception as e:
            _ = e

    def env_add_dirs(self, name, dirs):
        if not name or not dirs:
            return False
        _str = self.env_get(name)
        if dirs in _str:
            return True
        _str = '{};{}'.format(_str, dirs)
        self.env_set(name, _str)
        return True

    def env_add_exe(self, name, exe):
        return self.env_add_dirs(name, self.get_install_dir(exe))


if __name__ == '__main__':
    cp = Computer()
    cp.env_add_dirs('path', 'E:\\TEST\\123\\')
    # _dir = cp.get_install_dir('STM32CubeProgrammer.exe')
    # print(_dir)
    # _env = cp.env_get('path')
    # print(_env)
    # if _dir in _env:
    #     print('env exist')
    # else:
    #     cp.env_set('Path', '{};{}'.format(_env, _dir))
    # _env = cp.env_get('path')
    # print(_env)

    # print(os.system('STM32_Programmer_CLI -version'))
    # cp.env_set('Path', '{};{}'.format(_env, _dir))
    # print(os.system('STM32_Programmer_CLI -version'))
    # _env = cp.env_get('path')
    # print(_env)
