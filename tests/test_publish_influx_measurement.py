from enviroplusmonitor.sensors import weather

from .context import enviroplusmonitor


def test_publish_influx_measurement():
    assert weather.publish_influx_measurement() == None
