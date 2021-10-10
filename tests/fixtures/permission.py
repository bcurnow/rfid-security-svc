import pytest

from rfidsecuritysvc.model.permission import Permission


@pytest.fixture(scope='session')
def permissions():
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Permission(1, 'Open Door', 'Opens the door'),
        Permission(2, 'Perm 1', 'Permission 1'),
        Permission(3, 'Perm 2', 'Permission 2'),
        Permission(4, 'Perm 3', 'Permission 3'),
        Permission(5, 'Perm 4', 'Permission 4'),
        Permission(6, 'Perm 5', 'Permission 5'),
        Permission(7, 'No Desc', None),
        Permission(8, 'Default', None),
    ]


@pytest.fixture(scope='session')
def no_desc_permission(permissions):
    for p in permissions:
        if p.name == 'No Desc':
            return p


@pytest.fixture(scope='session')
def creatable_permission(permissions):
    return Permission(len(permissions) + 1, 'creatable name', 'creatable desc')


@pytest.fixture(scope='session')
def open_door_permission(permissions):
    for p in permissions:
        if p.name == 'Open Door':
            return p


@pytest.fixture(scope='session')
def default_permission(permissions):
    """ This permission should be used as the default (e.g. all guest, all media)"""
    for p in permissions:
        if p.name == 'Default':
            return p


@pytest.fixture(scope='session')
def permission_for_creatable_media_perm(permissions):
    """ This is the permission that should be used to create a creatable media_perm record."""
    for p in permissions:
        if p.name == 'Perm 5':
            return p


@pytest.fixture(autouse=True, scope='session')
def add_permission_helpers(monkeypatch_session):
    def convert(self):
        copy = self.__dict__.copy()
        del copy['id']
        return copy

    monkeypatch_session.setattr(Permission, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Permission, 'test_update', convert, raising=False)
