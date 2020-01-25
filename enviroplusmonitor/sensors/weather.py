__author__ = "Philip Cutler"

# import libraries
import logging
# import sys
from subprocess import PIPE, Popen

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


module_logger = logging.getLogger(configurationhandler.config['logging']['MODULE_LOGGER'])


bus = SMBus(1)

# BME280 temperature/pressure/humidity sensor
bme280 = BME280(i2c_dev=bus)

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

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

def sensor_readings():
    readings = {
        "temperature": unitregistryhandler.ureg.Quantity(compensated_temperature(), unitregistryhandler.ureg.degC),
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
