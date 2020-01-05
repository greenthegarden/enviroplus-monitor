__author__ = "Philip Cutler"

import time
from datetime import datetime, timedelta

from enviroplusmonitor.sensors import weather
from timeloop import Timeloop

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
tl = Timeloop()

# TODO: parameteratise time interval
@tl.job(interval=timedelta(seconds=60))
def sample_job_every_60s():
    weather.publish_influx_measurement()
