__author__ = "Philip Cutler"

# import libraries
import logging
import sys

# import internal modules
import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler

# import external packages
from bme280 import BME280
import pint
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


logger = logging.getLogger(__name__)

bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)

# import unit registry and definitions
ureg = pint.UnitRegistry()
ureg.load_definitions('../resources/default_en.txt')

def sensor_readings():
    readings = {
        "temperature": bme280.get_temperature() * ureg.degree_Celsius,
        "pressure": bme280.get_pressure() * ureg.hecto-pascal,
        "humidity_relative": bme280.get_humidity() * ureg.percent
    }
    return readings


def measurement():
    readings = sensor_readings()
    data = {
        "sensor": "bme280",
        "measurements": {
            "temperature": {
                "value": readings.get("temperature").magnitude,
                "units": readings.get("temperature").units
            }
            "humidity": {
                "value": readings.get("humidity").magnitude,
                "units": readings.get("humidity").units
            }
            "pressure": {
                "value": readings.get("pressure").magnitude,
                "units": readings.get("pressure").units
            }
        }
    }
    return data


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
