import pytest

from rfidsecuritysvc.model.media import Media


@pytest.fixture(scope='session')
def medias():
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Media('NOT AUTHORIZED', 'Not Authorized', 'This media should never be used in a media_perm record.'),
        Media('TEST FOR AUTHORIZED NO GUEST', 'test for authorized media without a guest media record', None),
        Media('TEST FOR GUESTMEDIA CREATION', 'test for GuestMedia creation', None),
        Media('TEST FOR MEDIAPERM CREATION', 'test for MediaPerm creation', None),
        Media('TEST MEDIA 1', 'test media 1', 'Media for testing (1)'),
        Media('TEST MEDIA 2', 'test media 2', 'Media for testing (2)'),
        Media('TEST MEDIA 3', 'test media 3', 'Media for testing (3)'),
        Media('TEST MEDIA 4', 'test media 4', 'Media for testing (4)'),
        Media('TEST MEDIA 5', 'test media 5', 'Media for testing (5)'),
        Media('TEST OPEN DOOR', 'test open door', 'This media will be assigned the permission Open Door'),
        Media('TEST WITHOUT DESC', 'test without desc', None),
    ]


@pytest.fixture(scope='session')
def creatable_media():
    return Media('CREATABLE ID', 'creatable name', 'creatable desc')


@pytest.fixture(scope='session')
def no_desc_media(medias):
    for m in medias:
        if m.id == 'TEST WITHOUT DESC':
            return m


@pytest.fixture(scope='session')
def no_prefs_media(no_desc_media):
    """ For use when building GuestMedia records """
    return no_desc_media


@pytest.fixture(scope='session')
def open_door_media(medias):
    for m in medias:
        if m.id == 'TEST OPEN DOOR':
            return m


@pytest.fixture(scope='session')
def not_authorized_media(medias):
    for m in medias:
        if m.id == 'NOT AUTHORIZED':
            return m


@pytest.fixture(scope='session')
def authorized_media_no_guest(medias):
    for m in medias:
        if m.id == 'TEST FOR AUTHORIZED NO GUEST':
            return m


@pytest.fixture(scope='session')
def media_for_creatable_media_perm(medias):
    """ This media should be used when creating a media_perm record."""
    for m in medias:
        if m.id == 'TEST FOR MEDIAPERM CREATION':
            return m


@pytest.fixture(scope='session')
def media_for_creatable_guest_media(medias):
    """ This media should be used when creating a guest_media record."""
    for m in medias:
        if m.id == 'TEST FOR GUESTMEDIA CREATION':
            return m


@pytest.fixture(scope='session')
def media_for_guests(medias):
    """ Each media returned should be associated with a guest """
    return medias[4:9]


@pytest.fixture(scope='session')
def media_without_guests(medias):
    """ Each media returned should NOT be associated with a guest """
    return medias[0:4]


@pytest.fixture(scope='session')
def media_for_permissions(medias):
    """ Each media returned should be associated with a permission """
    return medias[4:]


@pytest.fixture(autouse=True, scope='session')
def add_media_helpers(monkeypatch_session):
    def create(self):
        return self.to_json()

    def update(self):
        copy = self.to_json()
        del copy['id']
        return copy

    monkeypatch_session.setattr(Media, 'test_create', create, raising=False)
    monkeypatch_session.setattr(Media, 'test_update', update, raising=False)
