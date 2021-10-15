import pytest

from rfidsecuritysvc.model.color import Color


@pytest.fixture(scope='session')
def default_color():
    return Color(0xABCDEF)
