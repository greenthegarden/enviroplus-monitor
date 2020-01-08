import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)

influxdbc = None
database_name = configurationhandler.config["influxdb"]["INFLUXDB_DATABASE"]

#TODO: Needs configuration
def configure_client():
    global influxdbc
    influxdbc = InfluxDBClient(
        host=str(configurationhandler.config["influxdb"]["INFLUXDB_HOST"]),
        database=database_name
    )

    print("Create database: " + database_name)
    influxdbc.create_database(database_name)
    influxdbc.switch_database(database_name)
