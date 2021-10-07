from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.db import media_perm as table
from rfidsecuritysvc.model import permission
from rfidsecuritysvc.model import media
from rfidsecuritysvc.model import BaseModel


class MediaPerm(BaseModel):
    def __init__(self, id, media_id, media_name, media_desc, permission_id, permission_name, permission_desc):
        self.id = id
        self.media_id = media_id
        self.media_name = media_name
        self.media_desc = media_desc
        self.permission_id = permission_id
        self.permission_name = permission_name
        self.permission_desc = permission_desc


def get(id):
    return __model(table.get(id))


def get_by_media_and_perm(media_id, permission_name):
    return __model(table.get_by_media_and_perm(media_id, permission_name))


def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result


def create(media_id, permission_id):
    m = media.get(media_id)
    if not m:
        raise exception.MediaNotFoundError
    p = permission.get(permission_id)
    if not p:
        raise exception.PermissionNotFoundError

    return table.create(media_id, permission_id)


def delete(id):
    return table.delete(id)


def update(id, media_id, permission_id):
    return table.update(id, media_id, permission_id)


def __model(row):
    if not row:
        return
    return MediaPerm(row['id'],
                     row['media_id'],
                     row['media_name'],
                     row['media_desc'],
                     row['permission_id'],
                     row['permission_name'],
                     row['permission_desc']
                     )
