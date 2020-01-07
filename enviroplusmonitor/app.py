__author__ = "Philip Cutler"

"""
app.py
====================================
The core module of my example project

.. moduleauthor:: Philip Cuter <greenthegarden@gamil.com>
"""

import argparse
import logging
import os
import sys

from enviroplusmonitor.utilities import configurationhandler, logginghandler

logger = logging.getLogger(__name__)

default_configuration_file = str("." + "/" + "config.ini")


def parse_args(args):
    # """Parse the args from main."""
    parser = argparse.ArgumentParser(description="Enviroplus Monitor Project")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=False,
        default=default_configuration_file,
        help="Specify configuration file"
    )
    return parser.parse_args()



def run(parser):
    pre, ext = os.path.splitext(__file__)
    pre = os.path.basename(pre)

    print("\n\nRunning {pre}\n".format(pre=pre))

    config_file = parser.config

    print("Using configuration file {filename}".format(filename=config_file))
    configurationhandler.load_config(config_file)

    logginghandler.setup_logging(
        configurationhandler.config["logging"]["LOG_CFG_FILE"],
        configurationhandler.config["logging"]["LOG_CFG_VAR"],
        default_level=configurationhandler.config["logging"]["LOG_DEFAULT_LEVEL"],
    )

    # from enviroplusmonitor.utilities import mqttclienthandler

    # mqttclienthandler.configure_client()
    # mqttclienthandler.connect_to_broker()

    from enviroplusmonitor.utilities import influxdbclienthandler
    influxdbclienthandler.configure_client()

    from enviroplusmonitor.utilities import jobhandler

    jobhandler.tl.start(block=True)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    run(args)
