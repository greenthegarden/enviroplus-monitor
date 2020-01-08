# from .context import enviroplusmonitor

import enviroplusmonitor.app as app


def test_app_parse_args_config():
    args = app.parse_args(["-c", "test"])
    assert args.config == "test"


def test_app_parse_args_none():
    args = app.parse_args([])
    assert args.config == app.default_configuration_file
