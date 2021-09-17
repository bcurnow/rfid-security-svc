from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.db import association
from rfidsecuritysvc.model import media_perm
from rfidsecuritysvc.model import BaseModel
from rfidsecuritysvc.model import media
from rfidsecuritysvc.model import permission


class Association(BaseModel):
    def __init__(self, media_id, perm_name):
        self.media_id = media_id
        self.perm_name = perm_name


def get(media_id, perm_name):
    p = permission.get_by_name(perm_name)
    if not p:
        raise exception.PermissionNotFoundError

    mp = media_perm.get_by_media_and_perm(media_id, p.id)

    if mp:
        return Association(media_id, p.name)


def by_media(media_id):
    result = []
    for row in association.by_media(media_id):
        result.append(Association(row['media_id'], row['perm_name']))

    return result


def list():
    result = []
    for row in association.list():
        result.append(Association(row['media_id'], row['perm_name']))

    return result


def create(media_id, perm_name):
    m = media.get(media_id)
    if not m:
        raise exception.MediaNotFoundError
    p = permission.get_by_name(perm_name)
    if not p:
        raise exception.PermissionNotFoundError

    try:
        media_perm.create(media_id, p.id)
    except exception.DuplicateMediaPermError as e:
        raise exception.DuplicateAssociationError from e


def delete(media_id, perm_name):
    p = permission.get_by_name(perm_name)
    if not p:
        raise exception.PermissionNotFoundError

    mp = media_perm.get_by_media_and_perm(media_id, p.id)
    if not mp:
        return 0

    return media_perm.delete(mp.id)
