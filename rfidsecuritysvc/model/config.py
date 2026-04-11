from .base_model import BaseModel
from rfidsecuritysvc.db import config as table
from typing import Self
import sqlite3

class Config(BaseModel):
    def __init__(self: Self, key: str, value: str) -> None:
        self.key = key
        self.value = value


def get(key: str) -> Config:
    return __model(table.get(key))


def list() -> list[Config]:
    return [__model(row) for row in table.list()]


def create(key: str, value: str) -> Config:
    table.create(key, value)
    # We can just return what was passed in because there's no other primary key
    return Config(key, value)


def delete(key: str) -> int:
    return table.delete(key)


def update(key: str, value: str) -> int:
    return table.update(key, value)


def replace(key: str, value: str) -> int:
    return table.replace(key, value)


def __model(row: sqlite3.Row) -> Config:
    if row is None:
        return
    return Config(row['key'], row['value'])
