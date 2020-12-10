import pytest

import rfidsecuritysvc
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


@pytest.fixture(autouse=True)
def add_to_json_rw(monkeypatch):
    """
    Patches the rfidsecuritysvc.model.BaseModel class to add a to_json_rw method that returns
    only the keys that are not marked readonly in the API.
    Adds implementation to Permission and MediaPerm
    """

    def _read_only_keys(self):
        """
        Identifies any keys on this object that are defined read only at the API tier.
        Subclasses should override to specify their keys.
        """
        return []

    def to_json_rw(self):
        """ Returns a JSON compatible value stripped of keys which are defined read only at the API."""
        copy = self.__dict__.copy()
        for key in self._read_only_keys():
            del copy[key]

        return copy

    models_to_patch = {
        rfidsecuritysvc.model.permission.Permission: ['id'],
        rfidsecuritysvc.model.media_perm.MediaPerm: ['id'],
    }
    monkeypatch.setattr(rfidsecuritysvc.model.BaseModel, '_read_only_keys', _read_only_keys, raising=False)
    monkeypatch.setattr(rfidsecuritysvc.model.BaseModel, 'to_json_rw', to_json_rw, raising=False)

    for c, read_only_attrs in models_to_patch.items():
        monkeypatch.setattr(c, '_read_only_keys', lambda _: read_only_attrs, raising=False)
