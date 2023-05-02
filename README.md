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

## TODO
- Add job timeout with timeout decorator
- Use redis to store in between job cache
