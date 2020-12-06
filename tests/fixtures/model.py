import pytest


import rfidsecuritysvc
from rfidsecuritysvc.model.association import Association
from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.media_perm import MediaPerm
from rfidsecuritysvc.model.permission import Permission


@pytest.fixture(scope='session')
def configs(test_api_key):
    return [Config('ADMIN_API_KEY', test_api_key)]


@pytest.fixture(scope='session')
def creatable_config():
    return Config('creatable key', 'creatable value')


@pytest.fixture(scope='session')
def medias():
    return [
        Media('test media 1', 'test media 1', 'Media for testing (1)'),
        Media('test media 2', 'test media 2', 'Media for testing (2)'),
        Media('test media 3', 'test media 3', 'Media for testing (3)'),
        Media('test media 4', 'test media 4', 'Media for testing (4)'),
        Media('test media 5', 'test media 5', 'Media for testing (5)'),
        Media('test open door', 'test open door', 'This media will be assigned the permission Open Door'),
        Media('test without desc', 'test without desc', None),
    ]


@pytest.fixture(scope='session')
def creatable_media():
    return Media('creatable id', 'creatable name', 'creatable desc')



@pytest.fixture(scope='session')
def no_desc_media(medias):
    return medias[6]


@pytest.fixture(scope='session')
def permissions():
    return [
        Permission(1, 'Open Door', 'Opens the door'),
        Permission(2, 'Perm 1', 'Permission 1'),
        Permission(3, 'Perm 2', 'Permission 2'),
        Permission(4, 'Perm 3', 'Permission 3'),
        Permission(5, 'Perm 4', 'Permission 4'),
        Permission(6, 'Perm 5', 'Permission 5'),
        Permission(7, 'No Desc', None)
    ]



@pytest.fixture(scope='session')
def no_desc_permission(permissions):
    return permissions[6]


@pytest.fixture(scope='session')
def creatable_permission(permissions):
    return Permission(len(permissions) + 1, 'creatable name', 'creatable desc')


@pytest.fixture(scope='session')
def media_perms(medias, permissions):
    return [
        MediaPerm(1, medias[5].id, permissions[0].id),
        MediaPerm(2, 'test media 1', 2),
        MediaPerm(3, 'test media 2', 3),
        MediaPerm(4, 'test media 3', 4),
        MediaPerm(5, 'test media 4', 5),
        MediaPerm(6, 'test media 5', 6),
    ]


@pytest.fixture(scope='session')
def creatable_media_perm(media_perms):
    return MediaPerm(len(media_perms) + 1, 'test media 1', 3)


@pytest.fixture(scope='session')
def associations(medias, permissions):
    return [
        Association(medias[5].id, permissions[0].name),
        Association(medias[0].id, permissions[1].name),
        Association(medias[1].id, permissions[2].name),
        Association(medias[2].id, permissions[3].name),
        Association(medias[3].id, permissions[4].name),
        Association(medias[4].id, permissions[5].name),

    ]


@pytest.fixture(scope='session')
def creatable_association():
    return Association('test media 1', 'Perm 4')


@pytest.fixture(scope='session')
def open_door(medias, permissions, media_perms):
    """
    This fixture returns a tuple containing the Media, Permission and MediaPerm objects corresponding to the open door test
    data
    """
    return (medias[5], permissions[0], media_perms[0])


@pytest.fixture(scope='session')
def assert_model():
    def go(expected, actual):
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

    monkeypatch.setattr(rfidsecuritysvc.model.BaseModel, '_read_only_keys', _read_only_keys, raising=False)
    monkeypatch.setattr(rfidsecuritysvc.model.BaseModel, 'to_json_rw', to_json_rw, raising=False)

    # Create an override method for Permission and MediaPerm
    def remove_id(self):
        return ['id']

    monkeypatch.setattr(rfidsecuritysvc.model.permission.Permission, '_read_only_keys', remove_id, raising=False)
    monkeypatch.setattr(rfidsecuritysvc.model.media_perm.MediaPerm, '_read_only_keys', remove_id, raising=False)
