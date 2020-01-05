__author__ = "Philip Cutler"

"""
app.py
====================================
The core module of my example project

.. moduleauthor:: Philip Cuter <greenthegarden@gamil.com>
"""

import argparse
# import logging
import os
import sys
# import time
# from datetime import datetime, timedelta

# from timeloop import Timeloop
from enviroplusmonitor.utilities import (configurationhandler, logginghandler)


def main(argv):
    """
    Defines the methods to run.

    Returns:
        None
    """
    pre, ext = os.path.splitext(__file__)
    pre = os.path.basename(pre)

    print("\n\nRunning {pre}\n".format(pre=pre))

    default_configuration_file = "." + "/" + "config.ini"

    parser = argparse.ArgumentParser(description="Enviroplus Monitor Project")
    parser.add_argument(
        "-c",
        "--config",
        default=default_configuration_file,
        help="Specify configuration file",
    )
    args = parser.parse_args()

    print("Using configuration file {filename}".format(filename=args.config))
    configurationhandler.load_config(args.config)

    logginghandler.setup_logging(
        configurationhandler.config["logging"]["LOG_CFG_FILE"],
        configurationhandler.config["logging"]["LOG_CFG_VAR"],
        default_level=configurationhandler.config["logging"]["LOG_DEFAULT_LEVEL"],
    )

    from enviroplusmonitor.utilities import mqttclienthandler
    mqttclienthandler.configure_client()
    mqttclienthandler.connect_to_broker()

    from enviroplusmonitor.utilities import jobhandler

    jobhandler.tl.start(block=True)


if __name__ == "__main__":
    main(sys.argv[1:0])
