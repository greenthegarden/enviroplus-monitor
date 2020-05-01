__author__ = "Philip Cutler"

"""Publish gas measurements from Enviro+ Hat

   MICS6814 analog gas sensor (https://www.sgxsensortech.com/content/uploads/2015/02/1143_Datasheet-MiCS-6814-rev-8.pdf)

"""

# import libraries
import logging

# import internal modules
from enviroplusmonitor.utilities import (configurationhandler, homeassistanthandler, mqttclienthandler, schemahandler, unitregistryhandler)
from enviroplusmonitor.classes import (sensorRecord, mics6814MeasurementPayload, measurementRecord, configPayload)

# import external packages
from enviroplus import gas

module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)

sensor_label = str(configurationhandler.config["sensors"]["GAS_LABEL"])

def sensor_readings():
    """Get readings from each gas sensor on the MICS6814

    Returns:
        dict: 
    """
    all = gas.read_all()
    readings = {
        "oxidising": all.oxidising * unitregistryhandler.ureg.ppm,
        "reducing": all.reducing * unitregistryhandler.ureg.ppm,
        "nh3": all.nh3 * unitregistryhandler.ureg.ppm,
    }
    return readings


def measurement():
    """Structure sensor measurements into sensorRecord

    Returns:
        sensorRecord.SensorRecord:
    """
    readings = sensor_readings()
    module_logger.debug("readings: {output}".format(output=readings))
    # data = {
    #     "sensor": configurationhandler.config["sensors"]["GAS_LABEL"],
    #     "measurements": {
    #         "reducing": {
    #             "value": readings.get("reducing").magnitude,
    #             "units": readings.get("reducing").units,
    #         },
    #         "oxidising": {
    #             "value": readings.get("oxidising").magnitude,
    #             "units": readings.get("oxidising").units,
    #         },
    #         "nh3": {
    #             "value": readings.get("nh3").magnitude,
    #             "units": readings.get("nh3").units,
    #         },
    #     },
    # }
    measurements_from_readings = [
        { 'label': "oxidising", 'value': readings.get("oxidising").magnitude, 'units': str(readings.get("oxidising").units) },
        { 'label': "reducing", 'value': readings.get("reducing").magnitude, 'units': str(readings.get("reducing").units) },
        { 'label': "nh3", 'value': readings.get("nh3").magnitude, 'units': str(readings.get("nh3").units) }
    ]
    data = sensorRecord.SensorRecord(
        {
            'sensor': sensor_label,
            'measurements': measurements_from_readings
        }
    )
    module_logger.debug("data: {output}".format(output=schemahandler.to_json(data)))
    return data


def state_topic():
    """Define state topic for home assistant

    Returns:
        str: state topic
    """
    topic = str(homeassistanthandler.state_topic(sensor_label))
    return topic

# Configuration payload no1: {"device_class": "temperature", "name": "Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }
# def config_payload(device_class, unit_of_measurement, value_template):
#     name_elements = ["Enviro+", configurationhandler.config["enviroplus"]["id"], sensor_label, device_class.capitalize()]
#     config_payload_object = configPayload.ConfigPayload(
#         {
#             'device_class': str(device_class),
#             'name': " ".join(name_elements),
#             'state_topic': state_topic(),
#             'unit_of_measurement': str(unit_of_measurement),
#             'value_template': str(value_template)
#         }
#     )
#     module_logger.debug("config payload: {payload}".format(payload=to_json(config_payload_object)))
#     return to_json(config_payload_object)


def publish_configuration_topics():
    topic = homeassistanthandler.config_topic(sensor_label=sensor_label, measurement="oxidising")
    payload = homeassistanthandler.config_payload(device_class="None", measurement="oxidising", sensor_label=sensor_label, state_topic=state_topic(), unit_of_measurement="kO", value_template="{{ value_json.oxidising }}")
    module_logger.info("oxidising config topic: {topic}".format(topic=topic))
    module_logger.info("oxidising config payload: {payload}".format(payload=payload))
    mqttclienthandler.client.publish(topic, payload)
    topic = homeassistanthandler.config_topic(sensor_label=sensor_label, measurement="reducing")
    payload = homeassistanthandler.config_payload(device_class="None", measurement="reducing", sensor_label=sensor_label, state_topic=state_topic(), unit_of_measurement="kO", value_template="{{ value_json.reducing }}")
    module_logger.info("reducing config topic: {topic}".format(topic=topic))
    module_logger.info("reducing config payload: {payload}".format(payload=payload))
    mqttclienthandler.client.publish(topic, payload)
    topic = homeassistanthandler.config_topic(sensor_label=sensor_label, measurement="nh3")
    payload = homeassistanthandler.config_payload(device_class="None", measurement="nh3", sensor_label=sensor_label, state_topic=state_topic(), unit_of_measurement="kO", value_template="{{ value_json.nh3 }}")
    module_logger.info("nh3 config topic: {topic}".format(topic=topic))
    module_logger.info("nh3 config payload: {payload}".format(payload=payload))
    mqttclienthandler.client.publish(topic, payload)

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
#         + "reducing"
#         + "="
#         + str(round(measurements.get("reducing").get("value"), 2))
#         + ","
#         + "oxidising"
#         + "="
#         + str(round(measurements.get("oxidising").get("value"), 2))
#         + ","
#         + "nh3"
#         + "="
#         + str(round(measurements.get("nh3").get("value"), 2))
#     )
#     module_logger.info("Payload: {payload}".format(payload=payload))
#     mqttclienthandler.client.publish(TOPIC_STR, payload)

def publish_mqtt_discoverable_payload():
    readings = sensor_readings()
    # data = measurement()
    # module_logger.debug("data: {data}".format(data=data))
    # measurements = to_json(data.GetMeasurements())
    # module_logger.debug("measurements: {measurements}".format(measurements=measurements))
    payload = mics6814MeasurementPayload.Mics6814MeasurementPayload(
        {
            'oxidising': round(readings.get("oxidising").magnitude, 2),
            'reducing': round(readings.get("reducing").magnitude, 2),
            'nh3': round(readings.get("nh3").magnitude, 2)
        }
    )
    module_logger.info("Payload: {payload}".format(payload=schemahandler.to_json(payload)))
    mqttclienthandler.client.publish(state_topic(), schemahandler.to_json(payload))
