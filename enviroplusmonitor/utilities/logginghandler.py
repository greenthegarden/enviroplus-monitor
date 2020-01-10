__author__ = "Philip Cutler"


import json
import logging
import logging.config
import os
import sys

logger = logging.getLogger(__name__)


def setup_logging(default_path, env_key, default_level=logging.INFO):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.debug(logging.config.dictConfig(config))
    else:
        logging_numeric_level = getattr(logging, default_level.upper(), None)
        if not isinstance(logging_numeric_level, int):
            raise ValueError(
                "\n Logging level {lnl} not valid".format(lnl=logging_numeric_level)
            )
            sys.exit()
        logging.debug(logging.basicConfig(level=logging_numeric_level))
