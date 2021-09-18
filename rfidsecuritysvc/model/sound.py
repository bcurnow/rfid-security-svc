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



def get(id):
    return __model(table.get(id))


def list():
    result = []
    for row in table.list():
        result.append(__model_light(row))

    return result


def create(name, content):
    return table.create(name, content)


def delete(id):
    return table.delete(id)


def update(id, name):
    return table.update(id, name)


def __model(row):
    if not row:
        return
    c = __model_light(row)
    c.content = row['content']
    return c

def __model_light(row):
    return Sound(row['id'], row['name'])
