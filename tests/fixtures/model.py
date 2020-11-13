import pytest


from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.media_perm import MediaPerm
from rfidsecuritysvc.model.permission import Permission


@pytest.fixture
def configs(test_api_key):
    return [Config('ADMIN_API_KEY', test_api_key)]


@pytest.fixture
def medias():
    return [
        Media('test open door', 'test open door', 'This media will be assigned the permission Open Door'),
        Media('test media 1', 'test media 1', 'Media for testing (1)'),
        Media('test media 2', 'test media 2', 'Media for testing (2)'),
        Media('test media 3', 'test media 3', 'Media for testing (3)'),
        Media('test media 4', 'test media 4', 'Media for testing (4)'),
        Media('test media 5', 'test media 5', 'Media for testing (5)'),
    ]


@pytest.fixture
def permissions():
    """Returns a list of permission objects as defined in data.sql"""
    return [
        Permission(1, 'Open Door', 'Opens the door'),
        Permission(2, 'Perm 1', 'Permission 1'),
        Permission(3, 'Perm 2', 'Permission 2'),
        Permission(4, 'Perm 3', 'Permission 3'),
        Permission(5, 'Perm 4', 'Permission 4'),
        Permission(6, 'Perm 5', 'Permission 5'),
    ]


@pytest.fixture
def media_perms(medias, permissions):
    """Returns a list of media_perm objects as defined in data.sql minus the open door records"""
    return [
        MediaPerm(0, medias[0].id, permissions[0].id),
        MediaPerm(1, 'test media 1', 2),
        MediaPerm(2, 'test media 2', 3),
        MediaPerm(3, 'test media 3', 4),
        MediaPerm(4, 'test media 4', 5),
        MediaPerm(5, 'test media 5', 6),
    ]

@pytest.fixture
def open_door(medias, permissions, media_perms):
    """
    This fixture returns a tuple containing the Media, Permission and MediaPerm objects corresponding to the open door test
    data in data.sql
    """
    media = Media('test open door', 'test open door', 'This media will be assigned the permission Open Door')
    permission = Permission('Open Door', 'Opens the door')
    media_perm = MediaPerm('test open door', 1)
    return (medias[0], permissions[0], media_perms[0])


@pytest.fixture
def assert_model():
    def go(expected, actual):
        _assert_keys(expected, actual)
        _assert_keys(actual, expected)

    return go


def _assert_keys(one, two):
    for k,v in one.items():
        assert k in two
        assert two[k] == v
