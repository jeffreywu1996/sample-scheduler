import time
import logging
import wrapt_timeout_decorator as timeout_decorator

logger = logging.getLogger(__name__)


@timeout_decorator.timeout(10, use_signals=False)
def test_job_long():
    print('starting long job')
    time.sleep(20)
    print('ending long job')
