import pytest

from rfidsecuritysvc.model.media_perm import MediaPerm


@pytest.fixture(scope='session')
def media_perms(medias, open_door_media, open_door_permission, default_permission, not_authorized_media):
    # The DB will return these ordered by id, please build the list accordingly
    media_perms = []
    for i in range(len(medias)):
        if medias[i] != not_authorized_media:
            media_perms.append(MediaPerm(i,
                                         medias[i].id,
                                         medias[i].name,
                                         medias[i].desc,
                                         default_permission.id,
                                         default_permission.name,
                                         default_permission.desc))
    media_perms.append(MediaPerm(len(media_perms) + 1,
                                 open_door_media.id,
                                 open_door_media.name,
                                 open_door_media.desc,
                                 open_door_permission.id,
                                 open_door_permission.name,
                                 open_door_permission.desc))
    return media_perms


@pytest.fixture(scope='session')
def creatable_media_perm(media_perms, media_for_creatable_media_perm, permission_for_creatable_media_perm):
    return MediaPerm(len(media_perms) + 1,
                     media_for_creatable_media_perm.id,
                     media_for_creatable_media_perm.name,
                     media_for_creatable_media_perm.desc,
                     permission_for_creatable_media_perm.id,
                     permission_for_creatable_media_perm.name,
                     permission_for_creatable_media_perm.desc)
