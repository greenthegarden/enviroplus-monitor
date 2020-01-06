# from .context import enviroplusmonitor

from enviroplusmonitor import app
import sys

# Replace libraries by fake ones
import fake_rpi
sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

def test_app():
    assert app.main() == None


# fixtures
# paramertizer plus
