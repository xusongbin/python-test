
import os

test_path = 'E:\Development\项目资料'


def get_dirs(_dir):
    _list = []
    for root, dirs, files in os.walk(_dir):
        _list = dirs
        break
    # for i, d in enumerate(_list):
    #     _list[i] = _dir + '\\' + d
    return _list


if __name__ == '__main__':
    for a in get_dirs(test_path):
        print(a)
        try:
            os.rename(test_path + '\\' + a, test_path + '\\' + a.upper())
        except:
            pass
