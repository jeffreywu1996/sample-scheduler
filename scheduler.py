import time
import threading
import logging
from traceback import format_exc
from datetime import timedelta, datetime
from schedule import Scheduler

from jobs import fetch_jobs


logger = logging.getLogger(__name__)


class SafeScheduler(Scheduler):
    """
    An implementation of Scheduler that catches jobs that fail, logs their
    exception tracebacks as errors, optionally reschedules the jobs for their
    next run time, and keeps going.

    Use this to run jobs that may or may not crash without worrying about
    whether other jobs will run or if they'll crash the entire script.
    """

    def __init__(self, reschedule_on_failure=True, minutes_after_failure=0, seconds_after_failure=0):
        """
        If reschedule_on_failure is True, jobs will be rescheduled for their
        next run as if they had completed successfully. If False, they'll run
        on the next run_pending() tick.
        """
        self.reschedule_on_failure = reschedule_on_failure
        self.minutes_after_failure = minutes_after_failure
        self.seconds_after_failure = seconds_after_failure
        super().__init__()

    def _run_job(self, job):
        try:
            super()._run_job(job)
        except Exception:
            logger.exception(format_exc())
            if self.reschedule_on_failure:
                if self.minutes_after_failure != 0 or self.seconds_after_failure != 0:
                    logger.warn("Rescheduled in %s minutes and %s seconds." % (self.minutes_after_failure, self.seconds_after_failure))
                    job.last_run = None
                    job.next_run = datetime.now() + timedelta(minutes=self.minutes_after_failure, seconds=self.seconds_after_failure)
                else:
                    logger.warn("Rescheduled.")
                    job.last_run = datetime.now()
                    job._schedule_next_run()
            else:
                logger.warn("Job canceled.")
                self.cancel_job(job)


class BackgroundScheduler:
    def __init__(self, jobs: dict = None):
        logger.info('Starting scheduler...')
        self.stop_schedule_thread = threading.Event()
        self.schedule = SafeScheduler()
        if jobs:
            self.register_jobs(jobs)

    def register_jobs(self, jobs: dict):
        for job in jobs:
            self.schedule.every(job['interval']).seconds.do(job['job'])
            logger.info(f'Registered job: {job["job"].__name__} at {job["interval"]} seconds interval.')

    def __del__(self):
        self.stop_schedule_thread.set()  # Stop background job

    def start_in_background(self, refresh_interval=1):
        """
        Starts job in background
        https://schedule.readthedocs.io/en/stable/background-execution.html
        """

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not self.stop_schedule_thread.is_set():
                    try:
                        self.schedule.run_pending()
                    except Exception:
                        logger.exception('Exception found.')
                    time.sleep(refresh_interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        logger.info('Started scheduler in background...')
