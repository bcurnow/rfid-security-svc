from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.db import guest_media as table
from rfidsecuritysvc.model import guest, media, sound
from rfidsecuritysvc.model import BaseModel
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.sound import Sound


class GuestMedia(BaseModel):
    def __init__(self, id, guest, media, sound=None, color=None):
        self.id = id
        self.guest = guest
        self.media = media
        self.sound = sound
        self.color = color

    def to_json(self):
        copy = super().to_json()
        copy['guest'] = self.guest.to_json()
        copy['media'] = self.media.to_json()
        if self.sound:
            copy['sound'] = self.sound.to_json()
        if self.color:
            copy['color'] = self.color.to_json()
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

    guest_color = None
    if row['guest_color'] is not None:
        guest_color = Color(row['guest_color'])

    guest_sound = None
    if row['guest_sound'] is not None:
        guest_sound = Sound(row['guest_sound'], row['guest_sound_name'], row['guest_sound_last_update_timestamp'])

    g = guest.Guest(row['guest_id'],
                    row['guest_first_name'],
                    row['guest_last_name'],
                    guest_sound,
                    guest_color)
    m = media.Media(row['media_id'], row['media_name'], row['media_desc'])

    guest_media_color = None
    if row['color'] is not None:
        guest_media_color = Color(row['color'])

    guest_media_sound = None
    if row['sound_id'] is not None:
        guest_media_sound = Sound(row['sound_id'], row['sound_name'], row['sound_last_update_timestamp'])

    return GuestMedia(row['id'],
                      g,
                      m,
                      guest_media_sound,
                      guest_media_color)
