import pytest


import rfidsecuritysvc
from rfidsecuritysvc.model.media import Media


@pytest.fixture(scope='session')
def medias():
    return [
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
    return medias[6]
