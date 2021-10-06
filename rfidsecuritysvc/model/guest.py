from rfidsecuritysvc.db import guest as table
from rfidsecuritysvc.model import BaseModel


class Guest(BaseModel):
    def __init__(self, id, first_name, last_name, default_sound=None, default_color=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.default_sound = default_sound
        self.default_color = default_color


def get(id):
    return __model(table.get(id))


def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result


def create(first_name, last_name, default_sound=None, default_color=None):
    return table.create(first_name, last_name, default_sound, default_color)


def delete(id):
    return table.delete(id)


def update(id, first_name, last_name, default_sound=None, default_color=None):
    return table.update(id, first_name, last_name, default_sound, default_color)


def __model(row):
    if not row:
        return
    return Guest(
        row['id'],
        row['first_name'],
        row['last_name'],
        row['default_sound'],
        row['default_color']
        )
