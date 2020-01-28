__author__ = "Philip Cutler"

# import libraries
import board
import logging
import time

# import internal modules
import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import enviroplusmonitor.utilities.mqttclienthandler as mqttclienthandler
import enviroplusmonitor.utilities.unitregistryhandler as unitregistryhandler

# import external modules
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)


def sensor_readings():
  try:
    readings = {
      "temperature": unitregistryhandler.ureg.Quantity(dhtDevice.temperature, unitregistryhandler.ureg.degC),
      "humidity_relative": dhtDevice.humidity * unitregistryhandler.ureg.percent
    }
    return readings
  except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    module_logger.info(error.args[0])
    return None


def measurement():
  readings = sensor_readings()
  if readings is not None:
    data = {
      "sensor": str(configurationhandler.config["sensors"]["DHT22_LABEL"]),
      "measurements": {
        "temperature": {
          "value": readings.get("temperature").magnitude,
          "units": readings.get("temperature").units
        },
        "humidity": {
          "value": readings.get("humidity_relative").magnitude,
          "units": readings.get("humidity_relative").units
        }
      }
    }
    return data
  else:
    return None


TOPIC_STR = str(
  "enviroplus"
  + "/"
  + str(configurationhandler.config["enviroplus"]["id"])
  + "/"
  + str(configurationhandler.config["sensors"]["DHT22_LABEL"])
)
module_logger.info("Topic str: {topic}".format(topic=TOPIC_STR))


# weather,location=us-midwest,season=summer temperature=82
def publish_influx_payload():
  data = measurement()
  if data not None:
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
