from .test_job_1 import test_job_1
from .test_job_2 import test_job_2

_jobs = [
    {'job': test_job_1, 'interval': 10},
    {'job': test_job_2, 'interval': 20},
]


def fetch_jobs():
    return _jobs
