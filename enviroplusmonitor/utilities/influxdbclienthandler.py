import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)

influxdbc = None
database_name = configurationhandler.config["influxdb"]["INFLUXDB_DATABASE"]

# TODO: Needs configuration
def configure_client():
    global influxdbc
    influxdbc = InfluxDBClient(
        host=str(configurationhandler.config["influxdb"]["INFLUXDB_HOST"]),
        database=database_name,
    )

    print("Create database: " + database_name)
    influxdbc.create_database(database_name)
    influxdbc.switch_database(database_name)


# TODO: define test conditions for format
def format_measurement(data):
    fields = {key: value for key, value in data.get("measurements").items()}
    json_body = [
        {
            "measurement": data.get("sensor"),
            "tags": {
                "platform": "enviroplus",
                "id": str(configurationhandler.config["enviroplus"]["id"]),
            },
            "fields": fields,
        }
    ]
    return json_body


def publish_measurement(data):
    logger.info("Sensor data: {data}".format(data=data))
    json_data = format_measurement(data)
    logger.info("Publishing: {data}".format(data=json_data))
    try:
        influxdbc.write_points(format_measurement(data))
    except InfluxDBClientError as error:
        logger.info(error)
