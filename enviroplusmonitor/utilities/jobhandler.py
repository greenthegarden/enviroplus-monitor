__author__ = "Philip Cutler"

import logging
from datetime import timedelta

from enviroplusmonitor.sensors import gas, weather
from timeloop import Timeloop

logger = logging.getLogger(__name__)

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
tl = Timeloop()

# TODO: parameteratise time interval
@tl.job(interval=timedelta(seconds=60))
def sample_job_every_60s():
    logger.info("Publishing ...")
    weather.publish_measurement_to_influxdb()
    gas.publish_measurement_to_influxdb()
