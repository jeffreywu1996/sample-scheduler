# Sample Scheduler
A scheduler is a very common pattern we will find the need for. Here I am demostating how to use set up a background scheduler using the `schedule` package

```
jobs/         # Store jobs to schedule
scheduler.py  # Holds scheduler class
main.py       # Starts scheduler
```

## Get Started
```
pip3 install -r requirements.txt
python3 main.py
```

### Schedule a regular job
1. Create a new file like `test_job_1.py`, inside the file create a function like `test_job_1`.
2. In `__init__.py` file in `jobs`, import the function and register it in the `_jobs` dict
```
_jobs = [
    {'job': test_job_1, 'interval': 10},
    {'job': test_job_with_exceptions, 'interval': 60},
    {'job': test_job_long, 'interval': 30},

    {'job': FUNCTION_NAME_HERE, 'interval': INTERVAL_TO_CALL_JOB_IN_SEC}
]
```

### Schedule a job that can throw exceptions
All jobs automatically handle exceptions and silently swallow the error.

### Schedule a job with a timeout decorator
Sometimes a function can hang and block the scheduler. To prevent this, we want to add
a max_out timer to the function. Simply add a timeout decorator to the function.
```
@timeout_decorator.timeout(10, use_signals=False)
def test_job_long():
```

## TODO
- Add job timeout with timeout decorator (DONE)
- Use redis to store in between job cache
