import pytest

from rfidsecuritysvc.model.association import Association


@pytest.fixture(scope='session')
def associations(media_perms,
                 permissions,
                 open_door_media,
                 open_door_permission,
                 default_permission,
                 not_authorized_media):

    perm_map = dict((p.id, p.name) for p in permissions)
    associations = []
    for mp in media_perms:
        associations.append(Association(mp.media_id, perm_map[mp.perm_id]))
    return associations


@pytest.fixture(scope='session')
def creatable_association(medias, permissions):
    return Association(medias[0].id, permissions[1].name)
