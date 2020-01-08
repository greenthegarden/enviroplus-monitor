# from .context import enviroplusmonitor

# Replace libraries by fake ones
import sys
import fake_rpi

sys.modules["RPi"] = fake_rpi.RPi  # Fake RPi (GPIO)
sys.modules["smbus"] = fake_rpi.smbus  # Fake smbus (I2C)

from enviroplusmonitor.sensors import gas


def test_gas_sensor_readings():
    assert type(gas.sensor_readings()) == tuple
