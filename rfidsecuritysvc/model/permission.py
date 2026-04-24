from .base_model import BaseModel
from rfidsecuritysvc.db import permission as table
from typing import Self
import sqlite3

class Permission(BaseModel):
    def __init__(self: Self, id: int, name: str, desc: str = None) -> None:
        self.id = id
        self.name = name
        self.desc = desc

def get(id: int) -> Permission:
    return __model(table.get(id))


def get_by_name(name: str) -> Permission:
    return __model(table.get_by_name(name))


def list() -> list[Permission]:
    return [__model(row) for row in table.list()]


def create(name: str, desc: str = None) -> Permission:
    id = table.create(name, desc)
    return Permission(id, name, desc)


def delete(id: int) -> int:
    return table.delete(id)


def delete_by_name(name: str) -> int:
    return table.delete_by_name(name)


def update(id: int, name: str, desc: str = None) -> int:
    return table.update(id, name, desc)


def update_by_name(name: str, desc: str = None) -> int:
    return table.update_by_name(name, desc)


def __model(row: sqlite3.Row) -> Permission:
    if row is None:
        return
    return Permission(row['id'], row['name'], row['desc'])
