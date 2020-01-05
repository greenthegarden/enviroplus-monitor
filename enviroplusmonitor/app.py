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
from datetime import datetime, timedelta

from timeloop import Timeloop
from enviroplusmonitor.utilities import (configurationhandler, logginghandler)


# logger = logging.getLogger(__name__)

# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
# tl = Timeloop()

# @tl.job(interval=timedelta(seconds=2))
# def sample_job_every_2s():
#   print("2s job current time : {}".format(time.ctime()))

# @tl.job(interval=timedelta(seconds=5))
# def sample_job_every_5s():
#   print("5s job current time : {}".format(time.ctime()))


# @tl.job(interval=timedelta(seconds=60))
# def sample_job_every_60s():
#     print("60s job current time : {}".format(time.ctime()))
#     publish_influx_measurement()


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

    # from enviroplusmonitor.sensors import weather
    # weather.publish_influx_measurement()
    
    jobhanderl.tl.start(block=True)


if __name__ == "__main__":
    main(sys.argv[1:0])
