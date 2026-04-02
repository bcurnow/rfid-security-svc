from rfidsecuritysvc.db import media as table
from rfidsecuritysvc.model import BaseModel


class Media(BaseModel):
    def __init__(self, id, name, desc=None):
        self.id = id
        self.name = name
        self.desc = desc


def get(id):
    return __model(table.get(id))


def list(excludeAssociated=False):
    return [__model(row) for row in table.list(excludeAssociated)]


def create(id, name, desc=None):
    return table.create(id, name, desc)


def delete(id):
    return table.delete(id)


def update(id, name, desc=None):
    return table.update(id, name, desc)


def __model(row):
    if row is None:
        return
    return Media(row['id'], row['name'], row['desc'])
