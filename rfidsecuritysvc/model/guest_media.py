from . import guest, media, sound as sound_model
from .base_model import BaseModel
from .media import Media
from .guest import Guest
from .sound import Sound
from .color import Color
from rfidsecuritysvc.db import guest_media as table
from rfidsecuritysvc.exception import GuestNotFoundError, MediaNotFoundError, SoundNotFoundError
from typing import Self, Optional, Union, NoReturn
from types import ModuleType
import sqlite3

class GuestMedia(BaseModel):
    def __init__(self: Self, id: int, guest: Guest, media: Media, sound: Optional[Sound]  = None, color: Optional[Color] = None):
        self.id = id
        self.guest = guest
        self.media = media
        self.sound = sound
        self.color = color

    def to_json(self: Self) -> str:
        copy = super().to_json()
        copy['guest'] = self.guest.to_json()
        copy['media'] = self.media.to_json()
        if self.sound:
            copy['sound'] = self.sound.to_json()
        if self.color:
            copy['color'] = self.color.to_json()
        return copy


def get(id: int) -> GuestMedia:
    return __model(table.get(id))


def get_by_media(media_id: str) -> GuestMedia:
    return __model(table.get_by_media(media_id))


def list(guest_id: Optional[int]  = None) -> GuestMedia:
    return [__model(row) for row in table.list(guest_id)]


def create(guest_id: int, media_id: str, sound: Optional[int] = None, color: Optional[int] = None) -> int:
    g = _get_or_raise(guest, guest_id, GuestNotFoundError)
    m = _get_or_raise(media, media_id, MediaNotFoundError)
    s = None
    if sound:
        s = _get_or_raise(sound_model, sound, SoundNotFoundError)
    c = None
    if color:
        c = Color(color)

    id = table.create(guest_id, media_id, sound, color)
    
    # We have all the values, no need to look them up again
    return GuestMedia(id, g, m, s, c)


def delete(id: int) -> int:
    return table.delete(id)


def update(id: int, guest_id: int, media_id: str, sound: Optional[int] = None, color: Optional[int] = None) -> int:
    _get_or_raise(guest, guest_id, GuestNotFoundError)
    _get_or_raise(media, media_id, MediaNotFoundError)
    s = None
    if sound:
        _get_or_raise(sound_model, sound, SoundNotFoundError)

    return table.update(id, guest_id, media_id, sound, color)


def __model(row: sqlite3.Row) -> GuestMedia:
    if row is None:
        return

    guest_color = None
    if row['guest_color'] is not None:
        guest_color = Color(row['guest_color'])

    guest_sound = None
    if row['guest_sound'] is not None:
        guest_sound = Sound(row['guest_sound'], row['guest_sound_name'], row['guest_sound_last_update_timestamp'])

    g = guest.Guest(row['guest_id'], row['guest_first_name'], row['guest_last_name'], guest_sound, guest_color)
    m = media.Media(row['media_id'], row['media_name'], row['media_desc'])

    guest_media_color = None
    if row['color'] is not None:
        guest_media_color = Color(row['color'])

    guest_media_sound = None
    if row['sound'] is not None:
        guest_media_sound = Sound(row['sound'], row['sound_name'], row['sound_last_update_timestamp'])

    return GuestMedia(row['id'], g, m, guest_media_sound, guest_media_color)

def _get_or_raise(model: ModuleType, id: Union[int | str], error: Exception) -> Union[BaseModel | NoReturn]:
    result = model.get(id)
    if not result:
        raise error
    return result
