import logging

logger = logging.getLogger(__name__)


def test_job_with_exceptions():
    print('test job 2')
    raise Exception('test job has excpetion!')
