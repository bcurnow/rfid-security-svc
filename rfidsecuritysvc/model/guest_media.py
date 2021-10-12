from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.db import guest_media as table
from rfidsecuritysvc.model import guest, media, sound
from rfidsecuritysvc.model import BaseModel


class GuestMedia(BaseModel):
    def __init__(self, id, guest, media, sound_id=None, sound_name=None, color=None):
        self.id = id
        self.guest = guest
        self.media = media
        self.sound_id = sound_id
        self.sound_name = sound_name
        self.color = color
        if color is not None:
            # The color is stored as an integer, convert it to a hex string (e.g. FFFFFF)
            # and an HTML hex string (e.g. #ffffff) for use in various contexts
            self.color_hex = '{:X}'.format(color)
            self.color_html = f'#{"{:06x}".format(color)}'
        else:
            self.color_hex = None
            self.color_html = None

    def to_json(self):
        copy = super().to_json()
        copy['guest'] = self.guest.to_json()
        copy['media'] = self.media.to_json()
        return copy


def get(id):
    return __model(table.get(id))


def get_by_media(media_id):
    return __model(table.get_by_media(media_id))


def list(guest_id=None):
    result = []
    for row in table.list(guest_id):
        result.append(__model(row))

    return result


def create(guest_id, media_id, sound_id=None, color=None):
    g = guest.get(guest_id)
    if not g:
        raise exception.GuestNotFoundError
    m = media.get(media_id)
    if not m:
        raise exception.MediaNotFoundError
    if sound_id:
        s = sound.get(sound_id)
        if not s:
            raise exception.SoundNotFoundError

    return table.create(guest_id, media_id, sound_id, color)


def delete(id):
    return table.delete(id)


def update(id, guest_id, media_id, sound_id=None, color=None):
    g = guest.get(guest_id)
    if not g:
        raise exception.GuestNotFoundError
    m = media.get(media_id)
    if not m:
        raise exception.MediaNotFoundError
    if sound_id:
        s = sound.get(sound_id)
        if not s:
            raise exception.SoundNotFoundError
    return table.update(id, guest_id, media_id, sound_id, color)


def __model(row):
    if not row:
        return
    g = guest.Guest(row['guest_id'],
                    row['guest_first_name'],
                    row['guest_last_name'],
                    row['guest_default_sound'],
                    row['guest_default_sound_name'],
                    row['guest_default_color'])
    m = media.Media(row['media_id'], row['media_name'], row['media_desc'])
    return GuestMedia(row['id'],
                      g,
                      m,
                      row['sound_id'],
                      row['sound_name'],
                      row['color'])
