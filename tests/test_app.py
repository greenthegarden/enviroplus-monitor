from .context import enviroplusmonitor

# from enviroplusmonitor import app


def test_app():
    assert enviroplusmonitor.app.run() == None
