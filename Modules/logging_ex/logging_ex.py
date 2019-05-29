
from mylog import MyLog
from logging_ex_1 import test_out

log = MyLog()
log.set_logger('main')

if __name__ == '__main__':
    log.debug('12345')
    test_out()
