import logging

from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)


influxdbc = None


def configure_client():
    global influxdbc
    influxdbc = InfluxDBClient(
        host="192.168.1.90", database="temperature_monitoring"
    )
