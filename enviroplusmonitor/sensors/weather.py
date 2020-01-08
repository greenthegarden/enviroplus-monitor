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
    readings = {
        "temperature": bme280.get_temperature(),
        "pressure": bme280.get_pressure(),
        "humidity": bme280.get_humidity(),
    }
    return readings


# TODO: move to influxdbclienthandler (just pass data and sensor type)
def measurement():
    readings = sensor_readings()
    data = {
        "sensor": "bme280",
        "measurements": {
            "temperature": readings.get("temperature"),
            "humidity": readings.get("humidity"),
            "pressure": readings.get("pressure"),
        },
    }
    return data


# TODO: remove as moved to jobhandler
def publish_measurement_to_influxdb():
    json_body = measurement_influx_json()
    logger.info("Publishing: {data}".format(data=json_body))
    influxdbclienthandler.influxdbc.write_points(json_body)


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
