__author__ = "Philip Cutler"

# import libraries
import logging
import sys

# import internal modules
import enviroplusmonitor.sensors.mqttclienthandler as mqttclienthandler
import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.unitregistryhandler as unitregistryhandler

# import external packages
from bme280 import BME280
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


module_logger = logging.getLogger(configurationhandler.config['logging']['MODULE_LOGGER'])


bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)

def sensor_readings():
    readings = {
        "temperature": unitregistryhandler.ureg.Quantity(bme280.get_temperature(), unitregistryhandler.ureg.degC),
        "pressure": bme280.get_pressure() * unitregistryhandler.ureg.hectopascal,
        "humidity_relative": bme280.get_humidity() * unitregistryhandler.ureg.percent
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
            },
            "humidity": {
                "value": readings.get("humidity_relative").magnitude,
                "units": readings.get("humidity_relative").units
            },
            "pressure": {
                "value": readings.get("pressure").magnitude,
                "units": readings.get("pressure").units
            }
        }
    }
    return data


TOPIC_STR = str(
    "enviroplus"
    + "/"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "/"
    + "weather"
)
module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))


# weather,location=us-midwest,season=summer temperature=82
def publish_influx_payload():
    data = measurement()
    payload = str(
        str(data.get("sensor"))
        + ","
        + "platform="
        + "enviroplus"
        + ","
        + "id="
        + str(configurationhandler.config["enviroplus"]["id"])
        + " "
        + "temperature"
        + "="
        + str(round(data("measurements").get("temperature").get("value"), 2))
        + ","
        + "humidity"
        + "="
        + str(round(data("measurements").get("humidity_relative").get("value"), 2))
        + ","
        + "pressure"
        + "="
        + str(round(data("measurements").get("pressure").get("value"), 2))
    )
    module_logger.info("Payload: {payload}".format(payload=payload))
    mqttclienthandler.client.publish(TOPIC_STR, payload)
