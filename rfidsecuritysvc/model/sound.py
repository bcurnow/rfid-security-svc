import base64
from datetime import datetime, timezone
from .base_model import BaseModel
from rfidsecuritysvc.db import sound as table
from typing import Self
import sqlite3

class Sound(BaseModel):
    def __init__(self: Self, id: int, name: str, last_update_timestamp: str, content: str = None) -> None:
        self.id = id
        self.name = name
        # All time in the database is stored as a string in ISO8601 format in UTC, however,
        # it doesn't store the offset/timezone in the string so we need to add that information in
        t = datetime.fromisoformat(last_update_timestamp)
        t = t.replace(tzinfo=timezone.utc)
        self.last_update_timestamp = t.isoformat(timespec='seconds')
        self.content = content

    def to_json(self: Self) -> str:
        """Override the base method to ensure that we don't show binary content everywhere"""
        cp = super().to_json()
        del cp['content']
        return cp

    def to_json_with_content(self: Self) -> str:
        """This method must be explicitly called to get the content"""
        # In order to translate to JSON, this must be encoded first
        json = self.to_json()
        # Why not UTF-8? Because Base64 uses only ASCII characters
        # All ASCII characters are UTF-8
        json['content'] = base64.b64encode(self.content).decode('ascii')
        return json


def get(id: int) -> Sound:
    return __model(table.get(id))


def get_by_name(name: str) -> Sound:
    return __model(table.get_by_name(name))


def list() -> list[Sound]:
    return [_model_light(row) for row in table.list()]


def create(name: str, content: str) -> Sound:
    return table.create(name, content)


def delete(id: int) -> int:
    return table.delete(id)


def update(id: int, name: str, content: str = None) -> int:
    return table.update(id, name, content)


def __model(row: sqlite3.Row) -> Sound:
    if row is None:
        return
    c = _model_light(row)
    c.content = row['content']
    return c


def _model_light(row: sqlite3.Row) -> Sound:
    return Sound(row['id'], row['name'], row['last_update_timestamp'])
