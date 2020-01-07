# from .context import enviroplusmonitor

import enviroplusmonitor.app as app


def test_app_parse_args():
    args = app.parse_args(['-c', 'test'])
    assert args.config == 'test'
