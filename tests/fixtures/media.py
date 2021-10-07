import pytest

from rfidsecuritysvc.model.media import Media


@pytest.fixture(scope='session')
def medias():
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Media('NOT AUTHORIZED', 'Not Authorized', 'This media should never be used in a media_perm record.'),
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
    return medias[7]


@pytest.fixture(scope='session')
def open_door_media(medias):
    return medias[6]


@pytest.fixture(scope='session')
def not_authorized_media(medias):
    return medias[0]


@pytest.fixture(scope='session')
def media_for_creatable_media_perm(medias):
    """ This media should be used when creating a creable media_perm record."""
    return medias[4]
