from .context import enviroplusmonitor


def test_my_print():
    assert enviroplusmonitor.utilities.my_utils.my_print("one") == None
