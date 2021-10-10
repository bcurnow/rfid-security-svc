from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.db import media_perm as table
from rfidsecuritysvc.model import permission
from rfidsecuritysvc.model import media
from rfidsecuritysvc.model import BaseModel


class MediaPerm(BaseModel):
    def __init__(self, id, media, permission):
        self.id = id
        self.media = media
        self.permission = permission

    def to_json(self):
        copy = self.__dict__.copy()
        copy['media'] = self.media.to_json()
        copy['permission'] = self.permission.to_json()
        return copy


def get(id):
    return __model(table.get(id))


def get_by_media_and_perm(media_id, permission_name):
    return __model(table.get_by_media_and_perm(media_id, permission_name))


def list(media_id=None):
    result = []
    for row in table.list(media_id):
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
    m = media.Media(row['media_id'], row['media_name'], row['media_desc'])
    p = permission.Permission(row['permission_id'], row['permission_name'], row['permission_desc'])
    return MediaPerm(row['id'], m, p)
