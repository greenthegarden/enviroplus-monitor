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
            "measurement": "bme280",
            "tags": {
                "platform": "enviroplus",
                "id": str(1),
            },
            "fields": {
                "temperature": readings.temperature,
                "humidity": readings.humidity,
                "pressure": readings.pressure,
            }
        }
    ]
    influxdbclienthandler.influxdbc.write_points(json_body)
    