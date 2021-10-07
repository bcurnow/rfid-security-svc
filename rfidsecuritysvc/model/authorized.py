from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.model import BaseModel, media_perm
from rfidsecuritysvc.model.guest import Guest

class MediaConfig(BaseModel):
    def __init__(self, media_perm, guest, sound_id, sound_name, color):
        self.media_id = media_perm.media_id
        self.media_name = media_perm.media_name
        self.media_desc = media_perm.media_desc
        self.permission_id = media_perm.permission_id
        self.permission_name = media_perm.permission_name
        self.permission_desc = media_perm.permission_desc
        self.guest_id = guest.id
        self.guest_first_name = guest.first_name
        self.guest_last_name = guest.last_name
        self.sound_id = sound_id
        self.sound_name = sound_name
        self.color = color


def authorized(media_id, perm_name):
    try:
        mp = media_perm.get_by_media_and_perm(media_id, perm_name)
        if mp:
            return MediaConfig(mp,
                               Guest(-1, 'not yet implemented', 'not yet implemented'),
                               -1,
                               'not yet implemented',
                               0x000000)
    except exception.PermissionNotFoundError:
        return None
    except exception.MediaPermNotFoundError:
        return None
