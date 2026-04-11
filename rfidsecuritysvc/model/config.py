from .base_model import BaseModel
from rfidsecuritysvc.db import config as table


class Config(BaseModel):
    def __init__(self, key, value):
        self.key = key
        self.value = value


def get(key):
    return __model(table.get(key))


def list():
    return [__model(row) for row in table.list()]


def create(key, value):
    table.create(key, value)
    # We can just return what was passed in because there's no other primary key
    return Config(key, value)


def delete(key):
    return table.delete(key)


def update(key, value):
    return table.update(key, value)


def replace(key, value):
    return table.replace(key, value)


def __model(row):
    if row is None:
        return
    return Config(row['key'], row['value'])
