__author__ = "Philip Cutler"

import json
import logging

from subprocess import PIPE, Popen

# from jsonschema import validate
# from typing import Any, List
# from pydantic import BaseModel, ValidationError

# import internal modules
from enviroplusmonitor.utilities import (configurationhandler, mqttclienthandler, unitregistryhandler)
from enviroplusmonitor.classes import (bme280Measurement, bme280MeasurementPayload, measurementRecord, configPayload)
# import external packages
from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)


def to_json(object):
    return(json.dumps(object, default=lambda x: x.Serializable()))

def json_print(o):
    print(json.dumps(o, default=lambda x: x.Serializable()))

bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)

def get_cpu_temperature():
    """Return the CPU temperature using 

    Returns:
          float: cpu temperature
    """
    process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index("=") + 1 : output.rindex("'")])


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 1.95

cpu_temps = [get_cpu_temperature()] * 5


def compensated_temperature():
    """Compensation for CPU temperature

    Returns:
        number: compenstated temperature
    """
    cpu_temp = get_cpu_temperature()
    # Smooth out with some averaging to decrease jitter
    global cpu_temps
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    return raw_temp - ((avg_cpu_temp - raw_temp) / factor)


def sensor_readings():
    """Get readings from each sensor on the BME280

    Returns:
        dict: 
    """
    # try:
    temperature_reading = compensated_temperature()
    # except AttributeError as error:
    #     module_logger.error(error)
    # try:
    pressure_reading = bme280.get_pressure()
    # except AttributeError as error:
    #     module_logger.error(error)
    # try:
    humidity_reading = bme280.get_humidity()
    # except AttributeError as error:
    #     module_logger.error(error)
    module_logger.info("Get reading")
    readings = {
        "temperature": unitregistryhandler.ureg.Quantity(
            temperature_reading, unitregistryhandler.ureg.degC
        ),
        "pressure": pressure_reading * unitregistryhandler.ureg.hectopascal,
        "humidity_relative": humidity_reading * unitregistryhandler.ureg.percent,
    }
    return readings

def measurement():
    """Structure sensor measurements into Bme280Measurement

    Returns:
        bme280Measurement.Bme280Measurement:
    """
    readings = sensor_readings()
    module_logger.debug("readings: {output}".format(output=readings))
    # measurements_from_readings = [
    #     measurementRecord.MeasurementRecord(
    #         {
    #             'label': "temperature",
    #             'value': readings.get("temperature").magnitude,
    #             'units': str(readings.get("temperature").units),
    #         }
    #     ),
    #     measurementRecord.MeasurementRecord(
    #         {
    #             'label': "humidity",
    #             'value': readings.get("humidity_relative").magnitude,
    #             'units': str(readings.get("humidity_relative").units),
    #         }
    #     ),
    #     measurementRecord.MeasurementRecord(
    #         {
    #             'label': "pressure",
    #             'value': readings.get("pressure").magnitude,
    #             'units': str(readings.get("pressure").units),
    #         }
    #     ),
    # ]
    measurements_from_readings = [
        { 'label': "temperature", 'value': readings.get("temperature").magnitude, 'units': str(readings.get("temperature").units) },
        { 'label': "humidity", 'value': readings.get("humidity_relative").magnitude, 'units': str(readings.get("humidity_relative").units) },
        { 'label': "pressure", 'value': readings.get("pressure").magnitude, 'units': str(readings.get("pressure").units) }
    ]
    data = bme280Measurement.Bme280Measurement(
        {
            'sensor': "BME280",
            'measurements': measurements_from_readings
        }
    )
    module_logger.debug("data: {output}".format(output=to_json(data)))
    return data


# payloads for dynamic mqtt support for home assistant
# https://www.home-assistant.io/docs/mqtt/discovery/
# Configuration topic no1: homeassistant/sensor/sensorBedroomT/config
#  homeassistant/sensor/enviroplus/3/config
def state_topic():
    """Define state topic for home assistant

    Returns:
        str: state topic
    """
    return str(
        "homeassistant/sensor/enviroplus/" +
        str(configurationhandler.config["enviroplus"]["id"]) +
        "/" +
        str(configurationhandler.config["sensors"]["WEATHER_LABEL"]) +
        "/" +
        "state"
    )

def config_topic(reading):
    context = "homeassistant/sensor"
    sensor = "enviroplus"
    topic = str(
        context + "/" +
        sensor + "/" +
        str(configurationhandler.config["enviroplus"]["id"]) + "/" +
        str(configurationhandler.config["sensors"]["WEATHER_LABEL"]) + "/" +
        reading + "/" +
        "config"
        )
    module_logger.debug("config topic for {reading}: {topic}".format(reading=reading, topic=topic))
    return topic


# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
def config_payload(reading, name, unit_of_measurement, value_template, state_topic=state_topic()):
    config_payload_object = configPayload.ConfigPayload(
        {
            'device_class': str(reading),
            'name': str(name),
            'state_topic': str(state_topic),
            'unit_of_measurement': str(unit_of_measurement),
            'value_template': str(value_template)
        }
    )
    module_logger.debug("config payload: {payload}".format(payload=to_json(config_payload_object)))
    return to_json(config_payload_object)


# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
# config_payload_press = configPayload.ConfigPayload(
#     {
#         'device_class': "pressure",
#         'name': "Pressure",
#         'state_topic': state_topic(),
#         'unit_of_measurement': "MPa",
#         'value_template': "{{ value_json.pressure}}"
#     }
# )

# CONFIG_TOPIC_HUM = str(
#     "homeassistant/sensor"
#     + "/"
#     + "enviroplus"
#     + "_"
#     + str(configurationhandler.config["enviroplus"]["id"])
#     + "_"
#     + str(configurationhandler.config["sensors"]["WEATHER_LABEL"])
#     + "_"
#     + "humidity"
#     + "/"
#     + "config"
# )

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
# config_payload_hum = configPayload.ConfigPayload( 
#     {
#         'device_class': "humidity",
#         'name': "Humidity",
#         'state_topic': state_topic(),
#         'unit_of_measurement': "%",
#         'value_template': "{{ value_json.humidity}}"
#     }
# )

# TOPIC_STR = str(
#     "enviroplus"
#     + "/"
#     + str(configurationhandler.config["enviroplus"]["id"])
#     + "/"
#     + str(configurationhandler.config["sensors"]["WEATHER_LABEL"])
# )
# module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))

def publish_configuration_topics():
    # module_logger.info("Payload: {payload}".format(payload=payload))
    module_logger.info("temperature:")
    module_logger.info("config_topic: {topic}".format(topic=config_topic("temperature")))
    module_logger.info("config_payload: {payload}".format(payload=config_payload("temperature", "Temperature", "C", "{{value_json.temperature}}")))
    # mqttclienthandler.client.publish(CONFIG_TOPIC_TEMP, config_payload_temp_json)
    module_logger.info("pressure:")
    module_logger.info("config_topic: {topic}".format(topic=config_topic("pressure")))
    module_logger.info("config_payload: {payload}".format(payload=config_payload("pressure", "Pressure", "MPa", "{{ value_json.pressure}}")))
    # mqttclienthandler.client.publish(CONFIG_TOPIC_HUM, config_payload_hum_json)
    module_logger.info("humidity:")
    module_logger.info("config_topic: {topic}".format(topic=config_topic("humidity")))
    module_logger.info("config_payload: {payload}".format(payload=config_payload("humidity", "Humidity", "%", "{{ value_json.humidity}}")))
    # mqttclienthandler.client.publish(CONFIG_TOPIC_HUM, config_payload_hum_json)

# # weather,location=us-midwest,season=summer temperature=82
# def publish_influx_payload():
#     data = measurement()
#     measurements = data.get("measurements")
#     payload = str(
#         str(data.get("sensor"))
#         + ","
#         + "platform="
#         + "enviroplus"
#         + ","
#         + "id="
#         + str(configurationhandler.config["enviroplus"]["id"])
#         + " "
#         + "temperature"
#         + "="
#         + str(round((measurements.get("temperature")).get("value"), 2))
#         + ","
#         + "humidity"
#         + "="
#         + str(round((measurements.get("humidity")).get("value"), 2))
#         + ","
#         + "pressure"
#         + "="
#         + str(round((measurements.get("pressure")).get("value"), 2))
#     )
#     module_logger.info("Payload: {payload}".format(payload=payload))
#     mqttclienthandler.client.publish(TOPIC_STR, payload)

def publish_mqtt_discoverable_payload():
    readings = sensor_readings()
    # data = measurement()
    # module_logger.debug("data: {data}".format(data=data))
    # measurements = to_json(data.GetMeasurements())
    # module_logger.debug("measurements: {measurements}".format(measurements=measurements))
    payload = bme280MeasurementPayload.Bme280MeasurementPayload(
        {
            'temperature': round(readings.get("temperature").magnitude, 2),
            'humidity': round(readings.get("humidity_relative").magnitude, 2),
            'pressure': round(readings.get("pressure").magnitude, 2)
        }
    )
    module_logger.info("Payload: {payload}".format(payload=to_json(payload)))
    # mqttclienthandler.client.publish(STATE_TOPIC, payload)
