from rfidsecuritysvc.db import guest as table
from rfidsecuritysvc.model import BaseModel


class Guest(BaseModel):
    def __init__(self, id, first_name, last_name, default_sound=None, default_sound_name=None, default_color=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.default_sound = default_sound
        self.default_sound_name = default_sound_name
        self.default_color = default_color
        if default_color:
            # The default_color is stored as an integer, convert it to a hex string (e.g. FFFFFF)
            # and an HTML hex string (e.g. #ffffff) for use in various contexts
            self.default_color_hex = self.__to_hex(default_color).upper()
            self.default_color_html = f'#{self.__to_hex(default_color)}'
        else:
            self.default_color_hex = None
            self.default_color_html = None


    def __to_hex(self, value):
        return hex(value).lstrip('0x').rstrip('L')




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
        row['default_sound_name'],
        row['default_color'],
        )
