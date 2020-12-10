import pytest


import rfidsecuritysvc
from rfidsecuritysvc.model.association import Association


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
    return Association('TEST MEDIA 1', 'Perm 4')
