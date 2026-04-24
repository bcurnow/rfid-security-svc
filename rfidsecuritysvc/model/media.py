from .base_model import BaseModel
from rfidsecuritysvc.db import media as table
from typing import Self
import sqlite3

class Media(BaseModel):
    def __init__(self: Self, id: str, name: str, desc: str = None) -> None:
        self.id = id
        self.name = name
        self.desc = desc

def get(id: str) -> Media:
    return __model(table.get(id))


def list(exclude_associated: bool = False) -> list[Media]:
    return [__model(row) for row in table.list(exclude_associated)]


def create(id: str, name: str, desc: str = None) -> Media:
    id = table.create(id, name, desc)
    return Media(id, name, desc)


def delete(id: str) -> int:
    return table.delete(id)


def update(id: str, name: str, desc: str = None) -> int:
    return table.update(id, name, desc)


def __model(row: sqlite3.Row) -> Media:
    if row is None:
        return
    return Media(row['id'], row['name'], row['desc'])
