__author__ = "Philip Cutler"


import sys

from configobj import ConfigObj

config = None


def load_config(config_file):
    try:
        global config
        config = ConfigObj(str(config_file), raise_errors=True, file_error=True)
        # print("config: {config}".format(str(config)))
    except IOError:
        sys.exit(
            "Configuration file {config_file} not found".format(config_file=config_file)
        )
    except ConfigObj.ConfigObjError:
        sys.exit(
            "Invalid configuration file {config_file}".format(config_file=config_file)
        )
