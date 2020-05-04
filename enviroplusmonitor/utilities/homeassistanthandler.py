__author__ = "Philip Cutler"

import logging
from enviroplusmonitor.utilities import (configurationhandler, mqttclienthandler, schemahandler)
from enviroplusmonitor.classes import (configPayload)

module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)

# payloads for dynamic mqtt support for home assistant
# https://www.home-assistant.io/docs/mqtt/discovery/
# Configuration topic no1: homeassistant/sensor/sensorBedroomT/config


discovery_prefix = "homeassistant"
component = "sensor"

def node_id(sensor_label):
  """Generate node_id based on sensor_label

    Parameters:
      sensor_label:
    
    Returns:
      str: node_id
  """
  node_id_str = str(
    "enviroplus" + "_" +
    str(configurationhandler.config["enviroplus"]["id"]) + "_" +
    sensor_label
  )
  return node_id_str

# homeassistant/sensor/enviroplus3/state
# 
# homeassistant/sensor/enviroplus3BME280/state
def state_topic(sensor_label):
    """Define state topic for home assistant

    Parameters:
      sensor_label:

    Returns:
        str: state topic
    """
    topic_elements = [
      discovery_prefix,
      component,
      str(node_id(sensor_label)),
      "state"
    ]
    topic = mqttclienthandler.create_topic_from_list(topic_elements)
    module_logger.debug("state topic for {sensor}: {topic}".format(sensor=sensor_label, topic=topic))
    return topic

#  homeassistant/sensor/enviroplus3temperature/config
def config_topic(sensor_label, measurement):
    """Define config topic for home assistant

    Parameters:
      sensor_label:
      reading: data type

    Returns:
        str: state topic
    """
    # context = "homeassistant/sensor"
    # sensor = "enviroplus"
    # topic = str(
    #     context + "/" +
    #     sensor + "/" +
    #     str(configurationhandler.config["enviroplus"]["id"]) + "/" +
    #     str(configurationhandler.config["sensors"]["WEATHER_LABEL"]) + "/" +
    #     reading + "/" +
    #     "config"
    #     )
    topic_elements = [
      discovery_prefix,
      component,
      str(node_id(sensor_label) + "_" + measurement),
      "config"
    ]
    topic = mqttclienthandler.create_topic_from_list(topic_elements)
    module_logger.debug("config topic for {measurement} for sensor {sensor}: {topic}".format(measurement=measurement, sensor=sensor_label, topic=topic))
    return topic


def config_payload(device_class, measurement, sensor_label, state_topic, unit_of_measurement, value_template):
    name_elements = ["Enviro+", configurationhandler.config["enviroplus"]["id"], sensor_label, measurement]
    config_payload_object = configPayload.ConfigPayload(
        {
            'device_class': str(device_class),
            'name': " ".join(name_elements),
            'state_topic': state_topic,
            'unit_of_measurement': str(unit_of_measurement),
            'value_template': str(value_template)
        }
    )
    module_logger.debug("config payload: {payload}".format(payload=schemahandler.to_json(config_payload_object)))
    return schemahandler.to_json(config_payload_object)
