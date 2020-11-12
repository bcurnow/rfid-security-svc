from rfidsecuritysvc.db import config as table
from rfidsecuritysvc.model import BaseModel


class Config(BaseModel):
    def __init__(self, key, value):
        self.key = key
        self.value = value


def get(key):
    return __model(table.get(key))


def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result


def create(key, value):
    return table.create(key, value)


def delete(key):
    return table.delete(key)


def update(key, value):
    return table.update(key, value)


def __model(row):
    if not row:
        return
    return Config(row['key'], row['value'])
