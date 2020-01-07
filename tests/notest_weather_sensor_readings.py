# Replace libraries by fake ones
import sys
import fake_rpi

# sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

from enviroplusmonitor.sensors import weather

# from .context import enviroplusmonitor


def test_publish_influx_measurement():
    assert weather.publish_influx_measurement() == None
