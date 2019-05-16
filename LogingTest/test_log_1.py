
from test_log import logging

write_log = logging.getLogger(__name__)


def test_out():
    write_log.debug('67890')
