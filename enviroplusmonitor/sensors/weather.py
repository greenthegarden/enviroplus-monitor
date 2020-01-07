__author__ = "Philip Cutler"


import logging
import sys

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.influxdbclienthandler as influxdbclienthandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler
from bme280 import BME280


try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


logger = logging.getLogger(__name__)

bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)


def sensor_readings():
    readings = bme280.read_all()
    return readings


def measurement_influx_json():
    readings = sensor_readings()
    json_body = [
        {
            "measurement": "bme280",
            "tags": {"platform": "enviroplus", "id": str(1),},
            "fields": {
                "temperature": readings.temperature,
                "humidity": readings.humidity,
                "pressure": readings.pressure,
            },
        }
    ]
    return json_body


def publish_measurement_to_influxdb():
    influxdbclienthandler.influxdbc.write_points(measurement_influx_json())


# TOPIC_STR = str("tet")
# #     "enviroplus"
# #     + "/"
# #     + str(configurationhandler.config["enviroplus"]["id"])
# #     + "/"
# #     + "measurement"
# # )
# logger.info("Topic str: {topic}".format(topic=TOPIC_STR))


# # weather,location=us-midwest,season=summer temperature=82
# def publish_influx_measurement():
#     data = str(
#         "dht22,"
#         + "platform="
#         + "enviroplus"
#         + ","
#         + "id="
#         + str(configurationhandler.config["enviroplus"]["id"])
#         + " "
#         + "temperature"
#         + "="
#         + str(round(bme280.get_temperature(), 2))
#         + ","
#         + "humidity"
#         + "="
#         + str(round(bme280.get_humidity(), 2))
#     )
#     logger.info("Data: {data}".format(data=data))
#     mqttclienthandler.client.publish(TOPIC_STR, data)
