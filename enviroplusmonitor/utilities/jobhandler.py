__author__ = "Philip Cutler"

import logging
from datetime import timedelta

from enviroplusmonitor.sensors import dht22, gas, weather
from enviroplusmonitor.utilities import configurationhandler
# from enviroplusmonitor.utilities import influxdbclienthandler
from timeloop import Timeloop


module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)


# send configuration messages
def publish_configuration_topics():
    weather.publish_configuration_topics()
    gas.publish_configuration_topics()
    # if bool(configurationhandler.config["sensors"]["DHT22_ENABLE"]):
    #     dht22.publish_configuration_topics()


# set up timer
# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
tl = Timeloop()

@tl.job(
    interval=timedelta(
        seconds=int(configurationhandler.config["job"]["SAMPLE_PERIOD_SECS"])
    )
)
def publish_sensor_measurements():
    module_logger.info("Publishing ...")
    # try:
    weather.publish_mqtt_discoverable_payload()
    gas.publish_mqtt_discoverable_payload()

    # except (RuntimeError, TypeError, NameError):
    #     pass        
    # gas.publish_influx_payload()
    # if bool(configurationhandler.config["sensors"]["DHT22_ENABLE"]):
    #     dht22.publish_mqtt_discoverable_payload()
