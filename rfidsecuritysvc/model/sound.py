from rfidsecuritysvc.db import sound as table
from rfidsecuritysvc.model import BaseModel


class Sound(BaseModel):
    def __init__(self, id, file_name, content=None):
        self.id = id
        self.file_name = file_name
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


def create(file_name, content):
    return table.create(file_name, content)


def delete(id):
    return table.delete(id)


def update(id, file_name):
    return table.update(id, file_name)


def __model(row):
    if not row:
        return
    c = __model_light(row)
    c.content = row['content']
    return c

def __model_light(row):
    if not row:
        return
    return Sound(row['id'], row['file_name'])
