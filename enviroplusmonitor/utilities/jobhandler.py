__author__ = "Philip Cutler"

import logging
from datetime import timedelta

from enviroplusmonitor.sensors import gas, weather
from enviroplusmonitor.utilities import (configurationhandler,
                                         influxdbclienthandler)
from timeloop import Timeloop

module_logger = logging.getLogger(configurationhandler.config['logging']['MODULE_LOGGER'])

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
tl = Timeloop()

@tl.job(
    interval=timedelta(
        seconds=int(configurationhandler.config["job"]["JOB_INTERVAL_SECS"])
    )
)
def publish_sensor_measurements():
    module_logger.info("Publishing ...")
    weather.publish_influx_payload()
    gas.publish_influx_payload()
