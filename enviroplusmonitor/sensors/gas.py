__author__ = "Philip Cutler"

# import libraries
import logging

# import internal modules
import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.unitregistryhandler as unitregistryhandler

# import external packages
from enviroplus import gas

module_logger = logging.getLogger(configurationhandler.config['logging']['MODULE_LOGGER'])


def sensor_readings():
    all = gas.read_all()
    readings = {
        "reducing": all.reducing * unitregistryhandler.ureg.ppm,
        "oxidising": all.oxidising * unitregistryhandler.ureg.ppm,
        "nh3": all.nh3 * unitregistryhandler.ureg.ppm,
    }
    return readings

def measurement():
    readings = sensor_readings()
    data = {
        "sensor": "MICS6814",
        "measurements": {
            "reducing": {
                "value": readings.get("reducing").magnitude,
                "units": readings.get("reducing").units
            },
            "oxidising": {
                "value": readings.get("oxidising").magnitude,
                "units": readings.get("oxidising").units
            },
            "nh3": {
                "value": readings.get("nh3").magnitude,
                "units": readings.get("nh3").units
            }
        }
    }
    return data

TOPIC_STR = str(
    "enviroplus"
    + "/"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "/"
    + "gas"
)
module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))


# weather,location=us-midwest,season=summer temperature=82
def publish_influx_measurement():
    readings = sensor_readings()
    data = str(
        "MICS6814,"
        + "platform="
        + "enviroplus"
        + ","
        + "id="
        + str(configurationhandler.config["enviroplus"]["id"])
        + " "
        + "temperature"
        + "="
        + str(round(readings.get("temperature").magnitude, 2))
        + ","
        + "humidity"
        + "="
        + str(round(readings.get("humidity_relative").magnitude, 2))
        + ","
        + "pressure"
        + "="
        + str(round(readings.get("pressure"), 2))
    )
    module_logger.info("Data: {data}".format(data=data))
    mqttclienthandler.client.publish(TOPIC_STR, data)
