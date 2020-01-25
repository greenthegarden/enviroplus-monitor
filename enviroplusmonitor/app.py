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
import time
from pathlib import Path, PurePath

from enviroplusmonitor.utilities import configurationhandler, logginghandler

logger = logging.getLogger(__name__)

# see https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
resources_folder = Path("./enviroplusmonitor/resources/")

default_configuration_file = resources_folder / "config.ini"

def parse_args(args):
    # """Parse the args from main."""
    parser = argparse.ArgumentParser(description="Enviro+ Monitor Project")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=False,
        default=str(default_configuration_file),
        help="Specify configuration file",
    )
    return parser.parse_args()


def run(parser):

    pre, ext = os.path.splitext(__file__)
    pre = os.path.basename(pre)

    print("\n\nRunning {pre}\n".format(pre=pre))

    config_file = Path(parser.config)

    if not config_file.exists():
        sys.exit(
            "Configuration file {config_file} not found".format(config_file=config_file)
        )
    else:
        print("Using configuration file {filename}".format(filename=config_file))
        configurationhandler.load_config(config_file)

    # TODO: convert to method
    log_config_file = Path(configurationhandler.config["logging"]["LOG_CFG_FILE"])
    if not log_config_file.exists():
        log_config_file = PurePath(resources_folder, log_config_file)
        if not Path(log_config_file).exists():
            sys.exit("log config file {file} not found".format(file=log_config_file))
    logginghandler.setup_logging(
        log_config_file,
        configurationhandler.config["logging"]["LOG_CFG_VAR"],
        default_level=configurationhandler.config["logging"]["LOG_DEFAULT_LEVEL"],
    )

    from enviroplusmonitor.utilities import mqttclienthandler
    mqttclienthandler.configure_client()
    mqttclienthandler.connect_to_broker()

    # from enviroplusmonitor.utilities import influxdbclienthandler
    # influxdbclienthandler.configure_client()

    from enviroplusmonitor.utilities import unitregistryhandler
    unitregistryhandler.configure()

    # from enviroplusmonitor.sensors import weather
    # weather.init()

    from enviroplusmonitor.utilities import jobhandler
    jobhandler.tl.start(block=True)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    run(args)
