
import logging

import test_log_1

logging.basicConfig(
    filename='log_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
write_log = logging.getLogger('test_log')

if __name__ == '__main__':
    write_log.debug('12345')
    test_log_1.test_out()
