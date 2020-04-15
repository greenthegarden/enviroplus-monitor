# from .context import enviroplusmonitor

# Replace libraries by fake ones
import sys

import fake_rpi
from enviroplusmonitor.sensors import gas

sys.modules["RPi"] = fake_rpi.RPi  # Fake RPi (GPIO)
sys.modules["smbus"] = fake_rpi.smbus  # Fake smbus (I2C)


def test_gas_sensor_readings():
    assert type(gas.sensor_readings()) == tuple
