
from time import time, strftime, localtime
from traceback import format_exc
from myDriver.hhFile import Directory


def write_log(_data, file=None, directory=True, split=True):
    if not file:
        if split:
            file = strftime("%Y-%m-%d.txt", localtime())
        else:
            file = 'log.txt'
    if directory:
        _dir = 'log'
        if not Directory.exist(_dir):
            Directory.create(_dir)
        file = '{}/{}'.format(_dir, file)
    _save = strftime("%Y-%m-%d %H:%M:%S", localtime())
    _save += '.%03d ' % (int(time() * 1000) % 1000)
    _save += '{}'.format(_data)
    try:
        print(_save)
        with open(file, 'a+') as f:
            f.write(_save + '\n')
            f.flush()
    except Exception as e:
        print('LOG except:{}\n{}'.format(e, format_exc()))


class Log(object):
    def __init__(self):
        pass
