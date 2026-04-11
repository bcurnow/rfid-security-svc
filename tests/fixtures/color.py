import pytest

@pytest.fixture(scope='session')
def default_color():
    from rfidsecuritysvc.model.color import Color

    return Color(0xABCDEF)
