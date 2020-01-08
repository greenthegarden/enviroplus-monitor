__author__ = "Philip Cutler"

import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.influxdbclienthandler as influxdbclienthandler
from enviroplus import gas

logger = logging.getLogger(__name__)


def sensor_readings():
    readings = gas.read_all()
    return readings


# TODO: move to influxdbclienthandler (just pass data and sensor type)
def measurement():
    readings = sensor_readings()
    data = {
        "sensor": "MICS6814",
        "measurements": {
            "nh3": readings.nh3,
            "reducing": readings.reducing,
            "oxidising": readings.oxidising
        }
    }
    return data

# TODO: remove as moved to jobhandler
def publish_measurement_to_influxdb():
    json_body = measurement_influx_json()
    logger.info("Publishing: {data}".format(data=json_body))
    influxdbclienthandler.influxdbc.write_points(json_body)
