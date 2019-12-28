import time
from datetime import datetime, timedelta
from timeloop import Timeloop
from enviroplusmonitor.sensors import weather

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
tl = Timeloop()

@tl.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
  print("2s job current time : {}".format(time.ctime()))

@tl.job(interval=timedelta(seconds=5))
def sample_job_every_5s():
  print("5s job current time : {}".format(time.ctime()))

@tl.job(interval=timedelta(seconds=60))
def sample_job_every_60s():
    print("60s job current time : {}".format(time.ctime()))
    weather.publish_influx_measurement()
