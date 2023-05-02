from .test_job_1 import test_job_1
from .test_job_2_with_exceptions import test_job_with_exceptions
from .test_job_3_with_timeouts import test_job_long

_jobs = [
    {'job': test_job_1, 'interval': 10},
    {'job': test_job_with_exceptions, 'interval': 60},
    {'job': test_job_long, 'interval': 30},
]


def fetch_jobs():
    return _jobs
