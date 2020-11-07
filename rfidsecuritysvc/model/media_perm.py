from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.db import media_perm as table
from rfidsecuritysvc.model import permission
from rfidsecuritysvc.model import media
from rfidsecuritysvc.model import BaseModel

class MediaPerm(BaseModel):
    def __init__(self, id, media_id, perm_id):
        self.id = id
        self.media_id = media_id
        self.perm_id = perm_id

def get(id):
    return __model(table.get(id))

def get_by_media_and_perm(media_id, perm_id):
    return __model(table.get_by_media_and_perm(media_id, perm_id))

def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result  

def create(media_id, perm_id):
    m = media.get(media_id)
    if not m:
        raise exception.MediaNotFoundError
    p = permission.get(perm_id)
    if not p:
        raise exception.PermissionNotFoundError

    return table.create(media_id, perm_id)

def create_by_perm_name(media_id, perm_name):
    p = permission.get_by_name(perm_name)
    if p:
        return table.create(media_id, p.id)
    else:
        raise exception.PermissionNotFoundError

def delete(id):
    return table.delete(id)

def delete_by_media_and_perm(media_id, perm_id):
    return table.delete_by_media_and_perm(media_id, perm_id)

def update(id, media_id, perm_id):
    return table.update(id, media_id, perm_id)

def update_by_perm_name(media_id, perm_name):
    p = permission.get_by_name(perm_name)
    if p:
        return table.update(media_id, p.id)
    else:
        raise exception.PermissionNotFoundError

def __model(row):
    if not row: return
    return MediaPerm(row['id'], row['media_id'], row['perm_id'])
