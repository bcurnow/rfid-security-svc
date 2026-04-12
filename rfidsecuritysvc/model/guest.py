from .import sound as sound_model
from .base_model import BaseModel
from .sound import Sound
from .base_model import BaseModel
from .color import Color
from rfidsecuritysvc.exception import SoundNotFoundError
from rfidsecuritysvc.db import guest as table
from typing import Self
import sqlite3

class Guest(BaseModel):
    def __init__(self: Self, id: int, first_name: str, last_name: str, sound: int = None, color: int = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sound = sound
        self.color = color

    def to_json(self: Self) -> str:
        copy = super().to_json()
        if self.sound:
            copy['sound'] = self.sound.to_json()
        if self.color:
            copy['color'] = self.color.to_json()
        return copy


def get(id: int) -> Guest:
    return __model(table.get(id))


def list() -> list[Guest]:
    return [__model(row) for row in table.list()]


def create(first_name: str, last_name: str, sound: int = None, color: int = None) -> Guest:
    if sound:
        s = sound_model.get(sound)
        if not s:
            raise SoundNotFoundError
    id = table.create(first_name, last_name, sound, color)

    if sound is None and color is None:
        # We actually have everything we need to return now
        return Guest(id, first_name, last_name, None, None)
    
    # We don't have everything we need, instead of complicate sets of checking for sound and color and handling exceptions, etc. we'll just call get(id)
    return get(id)

def delete(id: int) -> int:
    return table.delete(id)


def update(id: int, first_name: str, last_name: str, sound: int = None, color: int = None) -> int:    
    if sound:
        s = sound_model.get(sound)
        if not s:
            raise SoundNotFoundError
    return table.update(id, first_name, last_name, sound, color)


def __model(row: sqlite3.Row) -> Guest:
    if row is None:
        return

    color = None
    if row['color'] is not None:
        color = Color(row['color'])

    sound = None
    if row['sound'] is not None:
        sound = Sound(row['sound'], row['sound_name'], row['sound_last_update_timestamp'])

    return Guest(row['id'], row['first_name'], row['last_name'], sound, color)
