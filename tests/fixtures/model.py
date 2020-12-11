import pytest

from rfidsecuritysvc.model import BaseModel


@pytest.fixture(scope='session')
def open_door(open_door_media, open_door_permission, open_door_media_perm):
    """
    This fixture returns a tuple containing the Media, Permission and MediaPerm objects corresponding to the open door test
    data
    """
    return (open_door_media, open_door_permission, open_door_media_perm)


@pytest.fixture(scope='session')
def assert_model():
    def go(expected, actual):
        if isinstance(expected, BaseModel):
            expected = expected.to_json()
        if isinstance(actual, BaseModel):
            actual = actual.to_json()
        _assert_keys(expected, actual)
        _assert_keys(actual, expected)

    return go


def _assert_keys(one, two):
    for k, v in one.items():
        assert k in two
        assert two[k] == v
