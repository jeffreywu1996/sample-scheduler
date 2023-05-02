import time
import logging

from scheduler import BackgroundScheduler
from jobs import fetch_jobs

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.register_jobs(fetch_jobs())
    scheduler.start_in_background()

    # Do some other tasks
    while True:
        time.sleep(1000000)
