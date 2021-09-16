import pytest

from rfidsecuritysvc.model.association import Association


@pytest.fixture(scope='session')
def associations(media_perms, permissions):

    perm_map = dict((p.id, p.name) for p in permissions)
    associations = []
    for mp in media_perms:
        associations.append(Association(mp.media_id, perm_map[mp.perm_id]))
    return associations




@pytest.fixture(scope='session')
def by_media_associations(open_door_media,
                          associations,
                          permissions):

    perm_map = dict((p.id, p.name) for p in permissions)
    results = []
    for a in associations:
        if a.media_id == open_door_media.id:
            results.append(a)

    return results


@pytest.fixture(scope='session')
def creatable_association(medias, permissions):
    return Association(medias[0].id, permissions[1].name)
