import pytest


import rfidsecuritysvc
from rfidsecuritysvc.model.media_perm import MediaPerm


@pytest.fixture(scope='session')
def media_perms(medias, permissions):
    return [
        MediaPerm(1, medias[5].id, permissions[0].id),
        MediaPerm(2, 'TEST MEDIA 1', 2),
        MediaPerm(3, 'TEST MEDIA 2', 3),
        MediaPerm(4, 'TEST MEDIA 3', 4),
        MediaPerm(5, 'TEST MEDIA 4', 5),
        MediaPerm(6, 'TEST MEDIA 5', 6),
    ]


@pytest.fixture(scope='session')
def creatable_media_perm(media_perms):
    return MediaPerm(len(media_perms) + 1, 'TEST MEDIA 1', 3)
