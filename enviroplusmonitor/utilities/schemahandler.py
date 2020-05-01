__author__ = "Philip Cutler"


import json
import logging

import enviroplusmonitor.utilities.configurationhandler as configurationhandler

module_logger = logging.getLogger(
    configurationhandler.config["logging"]["MODULE_LOGGER"]
)

def to_json(object):
    return(json.dumps(object, default=lambda x: x.Serializable()))

def json_print(o):
    print(json.dumps(o, default=lambda x: x.Serializable()))
