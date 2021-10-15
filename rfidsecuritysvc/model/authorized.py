from rfidsecuritysvc.model import BaseModel, media_perm, guest_media


class MediaConfig(BaseModel):
    def __init__(self, media_perm, guest, sound, color):
        self.media = media_perm.media
        self.permission = media_perm.permission
        self.guest = guest
        self.sound = sound
        self.color = color

    def to_json(self):
        copy = super().to_json()
        copy['media'] = self.media.to_json()
        copy['permission'] = self.permission.to_json()
        if self.guest is not None:
            copy['guest'] = self.guest.to_json()
        if self.sound is not None:
            copy['sound'] = self.sound.to_json()
        if self.color is not None:
            copy['color'] = self.color.to_json()
        return copy


def authorized(media_id, perm_name):
    mp = media_perm.get_by_media_and_perm(media_id, perm_name)
    if not mp:
        return
    # See if the media is associated with a guest
    gm = guest_media.get_by_media(media_id)

    color = None
    guest = None
    sound = None
    if gm:
        color = _resolveColor(gm)
        guest = gm.guest
        sound = _resolveSound(gm)

    return MediaConfig(mp, guest, sound, color)


def _resolveColor(gm):
    if gm.color:
        return gm.color
    # This can also be None but that's OK
    return gm.guest.color


def _resolveSound(gm):
    if gm.sound:
        return gm.sound
    return gm.guest.sound
