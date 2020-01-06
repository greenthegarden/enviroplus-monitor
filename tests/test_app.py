# from .context import enviroplusmonitor

from enviroplusmonitor import app
import sys

def test_app():
    assert app.main(None) == None


# fixtures
# paramertizer plus
