__author__ = "Philip Cutler"


import logging
import os
import sys
import time
import urllib.parse as urlparse
import uuid

import enviroplusmonitor.utilities.configurationhandler as configurationhandler
import paho.mqtt.client as mqttc

logger = logging.getLogger(__name__)

broker_attempt_count = 0

client = None


def get_broker_url():
    broker_url = urlparse.urlparse(
        "mqtt://"
        + str(configurationhandler.config["mqtt"]["MQTT_BROKER_IP"])
        + ":"
        + str(configurationhandler.config["mqtt"]["MQTT_BROKER_PORT"])
    )
    return broker_url


def on_connect(client, userdata, flags, rc):
    logger.debug("[Connect]")
    logger.info("Client: {client_id}".format(client_id=str(client._client_id)))
    logger.info("Result: {rc}".format(rc=mqttc.connack_string(rc)))
    if rc == 0:
        logger.info(
            "Connected to {host} on port {port}".format(
                host=client._host, port=client._port
            )
        )


def on_disconnect(client, userdata, rc):
    logger.debug("[Disconnect]")
    logger.info("Client: {client_id}".format(client_id=str(client._client_id)))
    logger.info("Result: {rc}".format(rc=mqttc.error_string(rc)))
    if rc > 0:
        logger.error(
            "Client {client} disconnected with error {error}".format(
                client=str(client), error=mqttc.error_string(rc)
            )
        )
        global broker_attempt_count
        if broker_attempt_count < int(
            configurationhandler.config["mqtt"]["MQTT_BROKER_ATTEMPTS"]
        ):
            time.sleep(int(configurationhandler.config["mqtt"]["MQTT_RECONNECT_DELAY"]))
            connect_to_broker()
            broker_attempt_count = broker_attempt_count + 1
        else:
            sys.exit(
                "Disconnected from broker with error {error}".format(
                    error=mqttc.error_string(rc)
                )
            )


# def on_log(client, userdata, level, buf):
#     logger.debug("[LOG] {0}".format(buf))


def on_publish(client, userdata, mid):
    logger.debug(
        "[Publish] message id: {message_id}".format(message_id=str(mid))
    )


def connect_to_broker():
    connected = False
    try:
        env_broker = urlparse.urlparse(
            os.environ.get("MQTT_BROKER_URL", get_broker_url())
        )
        logger.debug("Env Broker: {broker}".format(broker=env_broker))
    except Exception:
        env_broker = None
    if env_broker is not None:
        try:
            client.connect(env_broker.hostname, env_broker.port)
            connected = True
            logger.info(
                "Connect to broker at {broker}".format(broker=env_broker)
            )
            return
        except Exception as exc:
            logger.error("No connection to env broker")
    cfg_broker = get_broker_url()
    logger.debug("Cfg Broker: {broker}".format(broker=cfg_broker))
    if cfg_broker is not None:
        try:
            client.connect(cfg_broker.hostname, cfg_broker.port)
            connected = True
            logger.info(
                "Connect to broker at {broker}".format(broker=cfg_broker)
            )
            return
        except Exception as exc:
            logger.error("No connection to cfg broker")
    if connected is False:
        sys.exit("No connection to broker")


def configure_client():
    global client
    client_id = str(
        configurationhandler.config["mqtt"]["MQTT_CLIENT_ID"] + "_" + str(uuid.uuid4())
    )
    client = mqttc.Client(client_id)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    # client.on_log = on_log
    client.on_publish = on_publish
