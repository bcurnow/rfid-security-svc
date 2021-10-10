from rfidsecuritysvc.model import BaseModel, media_perm


class MediaConfig(BaseModel):
    def __init__(self, media_perm, guest, sound_id, sound_name, color):
        self.media = media_perm.media
        self.permission = media_perm.permission
        self.guest = guest
        self.sound_id = sound_id
        self.sound_name = sound_name
        self.color = color
        if color is not None:
            # The color is stored as an integer, convert it to a hex string (e.g. FFFFFF)
            # and an HTML hex string (e.g. #ffffff) for use in various contexts
            self.color_hex = format(color, 'X')
            self.color_html = f'#{format(color, "x")}'
        else:
            self.color_hex = None
            self.color_html = None

    def to_json(self):
        copy = self.__dict__.copy()
        copy['media'] = self.media.to_json()
        copy['permission'] = self.permission.to_json()
        if self.guest is not None:
            copy['guest'] = self.guest.to_json()
        return copy


def authorized(media_id, perm_name):
    mp = media_perm.get_by_media_and_perm(media_id, perm_name)
    if not mp:
        return
    return MediaConfig(mp, None, None, None, None)
