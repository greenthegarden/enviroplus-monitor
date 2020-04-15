import json
import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

logger = logging.getLogger(__name__)
module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)

influxdbc = None

database_name = configurationhandler.config["influxdb"]["INFLUXDB_DATABASE"]

# TODO: pass database name
def manage_database():
    global influxdbc
    module_logger.info("Manage database: " + database_name)
    try:
        influxdbc.create_database(database_name)
    except InfluxDBClientError:
        # Drop and create
        influxdbc.drop_database(database_name)
        influxdbc.create_database(database_name)
    influxdbc.switch_database(database_name)


# TODO: pass host and database info
def configure_client():
    global influxdbc
    influxdbc = InfluxDBClient(
        host=str(configurationhandler.config["influxdb"]["INFLUXDB_HOST"]),
        database=database_name,
    )
    manage_database()


# TODO: define test conditions for format
def format_measurement(data):
    fields = {
        key: value.get("value") for key, value in data.get("measurements").items()
    }
    module_logger.debug("influxdb fields: {fields}".format(fields=fields))
    data_point = [
        {
            "measurement": data.get("sensor"),
            "tags": {
                "platform": "enviroplus",
                "id": str(configurationhandler.config["enviroplus"]["id"]),
            },
            "fields": fields,
        }
    ]
    return json.dumps(data_point)


def publish_measurement(data):
    module_logger.debug("Sensor data: {data}".format(data=data))
    # try:
    influxdbc.write_points(json.loads(format_measurement(data)))
    # except InfluxDBClientError as error:
    #     module_logger.error(error)
    #     print(error)
    #     pass
