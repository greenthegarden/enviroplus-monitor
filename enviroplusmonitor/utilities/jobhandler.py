__author__ = "Philip Cutler"

import logging
from datetime import timedelta

from enviroplusmonitor.sensors import gas, weather
from enviroplusmonitor.utilities import configurationhandler
from timeloop import Timeloop

logger = logging.getLogger(__name__)

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
tl = Timeloop()

# TODO: parameteratise time interval
@tl.job(interval=timedelta(seconds=int(configurationhandler.config["job"]["JOB_INTERVAL_SECS"])))
def publish_sensor_measurements():
    logger.info("Publishing ...")
    weather.publish_measurement_to_influxdb()
    gas.publish_measurement_to_influxdb()
