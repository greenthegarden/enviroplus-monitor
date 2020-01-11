import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler

from influxdb import InfluxDBClient

module_logger = logging.getLogger(configurationhandler.config['logging']['MODULE_LOGGER'])

influxdbc = None

database_name = configurationhandler.config["influxdb"]["INFLUXDB_DATABASE"]

# TODO: pass database name
def manage_database():
    global influxdbc
    module_logger.info("Create database: " + database_name)
    module_logger.info(influxdbc.create_database(database_name))
    module_logger.info(influxdbc.switch_database(database_name))

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
    fields = {key: value.get("value") for key, value in data.get("measurements").items()}
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
    module_logger.info("Sensor data: {data}".format(data=data))
    json_data = format_measurement(data)
    module_logger.info("Publishing: {data}".format(data=json_data))
    try:
        influxdbc.write_points(format_measurement(data))
    except InfluxDBClientError as error:
        module_logger.info(error)
