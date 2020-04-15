__author__ = "Philip Cutler"

import json
import logging
import time

# import external modules
import adafruit_dht
# import libraries
import board
# import internal modules
import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler
import enviroplusmonitor.utilities.unitregistryhandler as unitregistryhandler

module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)


def sensor_readings():
    try:
        readings = {
            "temperature": unitregistryhandler.ureg.Quantity(
                dhtDevice.temperature, unitregistryhandler.ureg.degC
            ),
            "humidity_relative": dhtDevice.humidity * unitregistryhandler.ureg.percent,
        }
        return readings
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        module_logger.info(error.args[0])
        pass


def measurement():
    readings = sensor_readings()
    if readings is not None:
        data = {
            "sensor": str(configurationhandler.config["sensors"]["DHT22_LABEL"]),
            "measurements": {
                "temperature": {
                    "value": readings.get("temperature").magnitude,
                    "units": readings.get("temperature").units,
                },
                "humidity": {
                    "value": readings.get("humidity_relative").magnitude,
                    "units": readings.get("humidity_relative").units,
                },
            },
        }
        return data
    else:
        return None


# payloads for dynamic mqtt support for home assistant
# https://www.home-assistant.io/docs/mqtt/discovery/
# Configuration topic no1: homeassistant/sensor/sensorBedroomT/config
#  homeassistant/sensor/enviroplus/3/config
CONFIG_TOPIC_TEMP = str(
    "homeassistant/sensor"
    + "/"
    + "enviroplus"
    + "_"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "_"
    + str(configurationhandler.config["sensors"]["DHT22_LABEL"])
    + "_"
    + "temp"
    + "/"
    + "config"
)

STATE_TOPIC = "homeassistant/sensor/enviroplus/" + str(configurationhandler.config["enviroplus"]["id"]) + "/" +  str(configurationhandler.config["sensors"]["DHT22_LABEL"]) + "/" + "state"

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
CONFIG_PAYLOAD_TEMP_DICT = {
    "device_class": "temperature",
    "name": "Temperature",
    "state_topic": STATE_TOPIC,
    "unit_of_measurement": "°C",
    "value_template": "{{ value_json.temperature}}"
}
CONFIG_PAYLOAD_TEMP_JSON = json.dumps(CONFIG_PAYLOAD_TEMP_DICT)

CONFIG_TOPIC_HUM = str(
    "homeassistant/sensor"
    + "/"
    + "enviroplus"
    + "_"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "_"
    + str(configurationhandler.config["sensors"]["DHT22_LABEL"])
    + "_"
    + "humidity"
    + "/"
    + "config"
)

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
CONFIG_PAYLOAD_HUM_DICT = {
    "device_class": "humidity",
    "name": "Humidity",
    "state_topic": STATE_TOPIC,
    "unit_of_measurement": "%",
    "value_template": "{{ value_json.humidity}}"
}
CONFIG_PAYLOAD_HUM_JSON = json.dumps(CONFIG_PAYLOAD_HUM_DICT)

# Common state payload: { "temperature": 23.20, "humidity": 43.70 }

TOPIC_STR = str(
    "enviroplus"
    + "/"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "/"
    + str(configurationhandler.config["sensors"]["DHT22_LABEL"])
)
module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))

def publish_configuration_topics():
    # module_logger.info("Payload: {payload}".format(payload=payload))
    mqttclienthandler.client.publish(CONFIG_TOPIC_TEMP, CONFIG_PAYLOAD_TEMP_JSON)
    mqttclienthandler.client.publish(CONFIG_TOPIC_HUM, CONFIG_PAYLOAD_HUM_JSON)

# weather,location=us-midwest,season=summer temperature=82
def publish_influx_payload():
    data = measurement()
    if data is not None:
        measurements = data.get("measurements")
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
            + str(round((measurements.get("temperature")).get("value"), 2))
            + ","
            + "humidity"
            + "="
            + str(round((measurements.get("humidity")).get("value"), 2))
        )
        module_logger.info("Payload: {payload}".format(payload=payload))
        mqttclienthandler.client.publish(TOPIC_STR, payload)

def publish_mqtt_discoverable_payload():
    data = measurement()
    if data is not None:
        measurements = data.get("measurements")
        payload_dict = {
            "temperature": round((measurements.get("temperature")).get("value"), 2),
            "humidity": round((measurements.get("humidity")).get("value"), 2)
        }
        payload = json.dumps(payload_dict)
        module_logger.info("Payload: {payload}".format(payload=payload))
        mqttclienthandler.client.publish(STATE_TOPIC, payload)
