__author__ = "Philip Cutler"


import json
import logging
import logging.config
import os
import sys


def setup_logging(default_path, env_key, default_level=logging.INFO):
    """Setup logging configuration

    """
    path = str(default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        print("Using logging configuration file {file}".format(file=path))
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print("Logging configuration file {file} not found".format(file=path))
        logging_numeric_level = getattr(logging, default_level.upper(), None)
        if not isinstance(logging_numeric_level, int):
            raise ValueError(
                "\n Logging level {lnl} not valid".format(lnl=logging_numeric_level)
            )
            sys.exit()
        logging.basicConfig(level=logging_numeric_level)
