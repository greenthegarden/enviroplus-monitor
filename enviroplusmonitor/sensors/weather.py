__author__ = "Philip Cutler"


import logging
import sys

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.influxdbclienthandler as influxdbclienthandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler
# import fake_rpi
from bme280 import BME280

# sys.modules["smbus"] = fake_rpi.smbus  # Fake smbus (I2C)

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


logger = logging.getLogger(__name__)

bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)

TOPIC_STR = str("tet")
#     "enviroplus"
#     + "/"
#     + str(configurationhandler.config["enviroplus"]["id"])
#     + "/"
#     + "measurement"
# )
logger.info("Topic str: {topic}".format(topic=TOPIC_STR))


def sensor_readings():
    readings = bme280.read_all()
    return readings


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
        + ","
        + "humidity"
        + "="
        + str(round(bme280.get_humidity(), 2))
    )
    logger.info("Data: {data}".format(data=data))
    mqttclienthandler.client.publish(TOPIC_STR, data)


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
    influxdbclienthandler.influxdbc.write_points(json_body)
