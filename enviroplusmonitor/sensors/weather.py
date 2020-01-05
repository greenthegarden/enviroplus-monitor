__author__ = "Philip Cutler"


import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler

from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)

bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)

TOPIC_STR = str(
    "enviroplus"
    + "/"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "/"
    + "measurement"
)
module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))

# weather,location=us-midwest,season=summer temperature=82
def publish_influx_measurement():
    data = str(
        "dht22,"
        + "platform="
        + "enviroplus"
        + ","
        + "id="
        + str(configurationhandler.config["enviroplus"]["id"])
        + " "
        + "temperature"
        + "="
        + str(round(bme280.get_temperature(), 2))
        + " "
        + "humidity"
        + "="
        + str(round(bme280.get_humidity(), 2))
    )
    module_logger.info("Data: {data}".format(data=data))
    mqttclienthandler.client.publish(TOPIC_STR, data)
