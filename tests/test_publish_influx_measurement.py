from .context import enviroplusmonitor

from enviroplusmonitor.sensors import weather

def test_publish_influx_measurement():
    assert weather.publish_influx_measurement() == None
