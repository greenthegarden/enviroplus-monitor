__author__ = "Philip Cutler"


import sys

from configobj import ConfigObj

config = None


def load_config(config_file):
    try:
        global config
        config = ConfigObj(config_file, raise_errors=True, file_error=True)
    except IOError:
        print("exception")
        # write_config(config_file)
        # load_config(config_file)
    except ConfigObj.ConfigObjError:
        sys.exit(
            "Invalid configuration file {config_file}".format(config_file=config_file)
        )
