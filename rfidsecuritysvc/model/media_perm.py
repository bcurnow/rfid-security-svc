from . import media, permission
from .base_model import BaseModel
from .permission import Permission
from .media import Media
from rfidsecuritysvc.exception import MediaNotFoundError, PermissionNotFoundError
from rfidsecuritysvc.db import media_perm as table
from typing import Self
import sqlite3

class MediaPerm(BaseModel):
    def __init__(self: Self, id: int, media: Media, permission: Permission) -> None:
        self.id = id
        self.media = media
        self.permission = permission

    def to_json(self) -> str:
        copy = super().to_json()
        copy['media'] = self.media.to_json()
        copy['permission'] = self.permission.to_json()
        return copy


def get(id: int) -> MediaPerm:
    return __model(table.get(id))


def get_by_media_and_perm(media_id: str, permission_name: str) -> MediaPerm:
    return __model(table.get_by_media_and_perm(media_id, permission_name))


def list(media_id: str = None) -> list[MediaPerm]:
    return [__model(row) for row in table.list(media_id)]


def create(media_id: str, permission_id: int) -> int:
    m = media.get(media_id)
    if not m:
        raise MediaNotFoundError
    p = permission.get(permission_id)
    if not p:
        raise PermissionNotFoundError

    id = table.create(media_id, permission_id)
    return get(id)



def delete(id):
    return table.delete(id)


def update(id, media_id, permission_id):
    return table.update(id, media_id, permission_id)


def __model(row: sqlite3.Row) -> MediaPerm:    
    if row is None:
        return
    m = media.Media(row['media_id'], row['media_name'], row['media_desc'])
    p = permission.Permission(row['permission_id'], row['permission_name'], row['permission_desc'])
    return MediaPerm(row['id'], m, p)
