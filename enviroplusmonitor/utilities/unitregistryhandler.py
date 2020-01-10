import logging

import pint

logger = logging.getLogger(__name__)


ureg = None

def configure():
  global ureg
  # import unit registry and definitions
  ureg = pint.UnitRegistry()
  ureg.load_definitions('enviroplusmonitor/resources/default_en.txt')
