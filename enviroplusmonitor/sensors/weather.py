__author__ = "Philip Cutler"

import json
import logging

from subprocess import PIPE, Popen

from jsonschema import validate
from typing import Any, List
from pydantic import BaseModel, ValidationError

# import internal modules
import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler
import enviroplusmonitor.utilities.unitregistryhandler as unitregistryhandler
# import external packages
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

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    """Return the CPU temperature using 

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index("=") + 1 : output.rindex("'")])


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 1.95

cpu_temps = [get_cpu_temperature()] * 5


def compensated_temperature():
    cpu_temp = get_cpu_temperature()
    # Smooth out with some averaging to decrease jitter
    global cpu_temps
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    return raw_temp - ((avg_cpu_temp - raw_temp) / factor)


class ConfigPayload(BaseModel):
  device_class: str
  name: str
  state_topic: str
  unit_of_measurement: str
  value_template: str

class Measurement(BaseModel):
  label: str
  value: float
  units: Any

class Bme280Measurement(BaseModel):
  sensor: str = configurationhandler.config["sensors"]["WEATHER_LABEL"]
  measurements: List[Measurement]

class Bme280MeasurementPayload(BaseModel):
  temperature: float
  humidity: float
  pressure: float

def sensor_readings():
    readings = {
        "temperature": unitregistryhandler.ureg.Quantity(
            compensated_temperature(), unitregistryhandler.ureg.degC
        ),
        "pressure": bme280.get_pressure() * unitregistryhandler.ureg.hectopascal,
        "humidity_relative": bme280.get_humidity() * unitregistryhandler.ureg.percent,
    }
    return readings


def measurement():
    readings = sensor_readings()
    data = Bme280Measurement(
        measurements = [
            Measurement(
                label =  "temperature",
                value = readings.get("temperature").magnitude,
                units = readings.get("temperature").units,
            ),
            Measurement(
                label = "humidity",
                value = readings.get("humidity_relative").magnitude,
                units = readings.get("humidity_relative").units,
            ),
            Measurement(
                label = "pressure",
                value = readings.get("pressure").magnitude,
                units = readings.get("pressure").units,
            ),
        ]
    )
    return data

# payloads for dynamic mqtt support for home assistant
# https://www.home-assistant.io/docs/mqtt/discovery/
# Configuration topic no1: homeassistant/sensor/sensorBedroomT/config
#  homeassistant/sensor/enviroplus/3/config
STATE_TOPIC = str(
    "homeassistant/sensor/enviroplus/" +
    str(configurationhandler.config["enviroplus"]["id"]) +
    "/" +
    str(configurationhandler.config["sensors"]["WEATHER_LABEL"]) +
    "/" +
    "state"
)

CONFIG_TOPIC_TEMP = str(
    "homeassistant/sensor"
    + "/"
    + "enviroplus"
    + "_"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "_"
    + str(configurationhandler.config["sensors"]["WEATHER_LABEL"])
    + "_"
    + "temp"
    + "/"
    + "config"
)

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
config_payload_temp = ConfigPayload(
  device_class = 'temperature',
  name = "Temperature",
  state_topic = STATE_TOPIC,
  unit_of_measurement = "°C",
  value_template = "{{ value_json.temperature}}"
)
config_payload_temp_json = json.dumps(config_payload_temp.dict())

CONFIG_TOPIC_PRESS = str(
    "homeassistant/sensor"
    + "/"
    + "enviroplus"
    + "_"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "_"
    + str(configurationhandler.config["sensors"]["WEATHER_LABEL"])
    + "_"
    + "pressure"
    + "/"
    + "config"
)

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
config_payload_press = ConfigPayload(
  device_class = "pressure",
  name = "Pressure",
  state_topic = STATE_TOPIC,
  unit_of_measurement = "MPa",
  value_template = "{{ value_json.pressure}}"
)
config_payload_press_json = json.dumps(config_payload_press.dict())


CONFIG_TOPIC_HUM = str(
    "homeassistant/sensor"
    + "/"
    + "enviroplus"
    + "_"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "_"
    + str(configurationhandler.config["sensors"]["WEATHER_LABEL"])
    + "_"
    + "humidity"
    + "/"
    + "config"
)

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
config_payload_hum = ConfigPayload(
  device_class = "humidity",
  name = "Humidity",
  state_topic = STATE_TOPIC,
  unit_of_measurement = "%",
  value_template = "{{ value_json.humidity}}"
)
config_payload_hum_json = json.dumps(config_payload_hum.dict())


TOPIC_STR = str(
    "enviroplus"
    + "/"
    + str(configurationhandler.config["enviroplus"]["id"])
    + "/"
    + str(configurationhandler.config["sensors"]["WEATHER_LABEL"])
)
module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))

def publish_configuration_topics():
    # module_logger.info("Payload: {payload}".format(payload=payload))
    module_logger.info("CONFIG_TOPIC_TEMP: {topic}".format(topic=CONFIG_TOPIC_TEMP))
    module_logger.info("config_payload_temp_json: {payload}".format(payload=config_payload_temp_json))
    mqttclienthandler.client.publish(CONFIG_TOPIC_TEMP, config_payload_temp_json)
    module_logger.info("CONFIG_TOPIC_PRESS: {topic}".format(topic=CONFIG_TOPIC_PRESS))
    module_logger.info("config_payload_press_json: {payload}".format(payload=config_payload_press_json))
    mqttclienthandler.client.publish(CONFIG_TOPIC_PRESS, config_payload_press_json)
    module_logger.info("CONFIG_TOPIC_HUM: {topic}".format(topic=CONFIG_TOPIC_HUM))
    module_logger.info("config_payload_hum_json: {payload}".format(payload=config_payload_hum_json))
    mqttclienthandler.client.publish(CONFIG_TOPIC_HUM, config_payload_hum_json)

# weather,location=us-midwest,season=summer temperature=82
def publish_influx_payload():
    data = measurement()
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
        + ","
        + "pressure"
        + "="
        + str(round((measurements.get("pressure")).get("value"), 2))
    )
    module_logger.info("Payload: {payload}".format(payload=payload))
    mqttclienthandler.client.publish(TOPIC_STR, payload)

def publish_mqtt_discoverable_payload():
    data = measurement()
    measurements = data.get("measurements")
    payload = Bme280MeasurementPayload(
        temperature = round((measurements.get("temperature")).get("value"), 2),
        humidity = round((measurements.get("humidity")).get("value"), 2),
        pressure = round((measurements.get("humidity")).get("value"), 2)
    )
    module_logger.info("Payload: {payload}".format(payload=json.dump(payload.dict())))
    mqttclienthandler.client.publish(STATE_TOPIC, payload)
