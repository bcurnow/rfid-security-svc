from rfidsecuritysvc.db import guest as table
from rfidsecuritysvc import exception
from rfidsecuritysvc.model import BaseModel, sound as sound_model
from rfidsecuritysvc.model.sound import Sound, to_sound_timestamp
from rfidsecuritysvc.model.color import Color


class Guest(BaseModel):
    def __init__(self, id, first_name, last_name, sound=None, color=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sound = sound
        self.color = color

    def to_json(self):
        copy = super().to_json()
        if self.sound:
            copy['sound'] = self.sound.to_json()
        if self.color:
            copy['color'] = self.color.to_json()
        return copy


def get(id):
    return __model(table.get(id))


def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result


def create(first_name, last_name, sound=None, color=None):
    if sound:
        s = sound_model.get(sound)
        if not s:
            raise exception.SoundNotFoundError
    return table.create(first_name, last_name, sound, color)


def delete(id):
    return table.delete(id)


def update(id, first_name, last_name, sound=None, color=None):
    if sound:
        s = sound_model.get(sound)
        if not s:
            raise exception.SoundNotFoundError
    return table.update(id, first_name, last_name, sound, color)


def __model(row):
    if not row:
        return

    color = None
    if row['color'] is not None:
        color = Color(row['color'])

    sound = None
    if row['sound'] is not None:
        sound = Sound(row['sound'], row['sound_name'], to_sound_timestamp(row['sound_last_update_timestamp']))

    return Guest(
        row['id'],
        row['first_name'],
        row['last_name'],
        sound,
        color)
