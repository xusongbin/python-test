
from mylog import MyLog

log = MyLog()
log.set_logger('test')


def test_out():
    log.debug('67890')
