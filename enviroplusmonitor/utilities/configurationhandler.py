__author__ = "Philip Cutler"


import logging
import sys

from configobj import ConfigObj

config = None

logger = logging.getLogger(__name__)


def load_config(config_file):
    try:
        global config
        config = ConfigObj(config_file, raise_errors=True, file_error=True)
    except IOError:
        logger.exception("Exception occurred")
    except ConfigObj.ConfigObjError:
        sys.exit(
            "Invalid configuration file {config_file}".format(config_file=config_file)
        )
