__author__ = "Philip Cutler"

import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.influxdbclienthandler as influxdbclienthandler
from enviroplus import gas

logger = logging.getLogger(__name__)


def sensor_readings():
    readings = gas.read_all()
    return readings


def measurement_influx_json():
    readings = sensor_readings()
    json_body = [
        {
            "measurement": "MICS6814",
            "tags": {"platform": "enviroplus", "id": str(1)},
            "fields": {
                "nh3": readings.nh3,
                "reducing": readings.reducing,
                "oxidising": readings.oxidising
            }
        }
    ]
    return json_body

def publish_measurement_to_influxdb():
    json_body = measurement_influx_json()
    logger.info("Publishing: {data}".format(data=json_body))
    influxdbclienthandler.influxdbc.write_points(json_body)
