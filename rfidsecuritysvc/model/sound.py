import base64

from rfidsecuritysvc.db import sound as table
from rfidsecuritysvc.model import BaseModel


class Sound(BaseModel):
    def __init__(self, id, name, content=None):
        self.id = id
        self.name = name
        self.content = content

    def to_json(self):
        """Override the base method to ensure that we don't show binary content everywhere"""
        cp = self.__dict__.copy()
        del cp['content']
        return cp

    def to_json_with_content(self):
        """This method must be explicitly called to get the content"""
        # In order to translate to JSON, this must be encoded first
        cp = self.__dict__.copy()
        # Why not UTF-8? Because Base64 uses only ASCII characters
        # All ASCII characters are UTF-8
        cp['content'] = base64.b64encode(cp['content']).decode('ascii')
        return cp


def get(name):
    return __model(table.get(name))


def list():
    result = []
    for row in table.list():
        result.append(__model_light(row))

    return result


def create(name, content):
    return table.create(name, content)


def delete(id):
    return table.delete(id)


def update(id, name, content=None):
    return table.update(id, name, content)


def __model(row):
    if not row:
        return
    c = __model_light(row)
    c.content = row['content']
    return c


def __model_light(row):
    return Sound(row['id'], row['name'])
