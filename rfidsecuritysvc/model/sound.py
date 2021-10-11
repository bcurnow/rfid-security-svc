import base64
from datetime import datetime, timezone

from rfidsecuritysvc.db import sound as table
from rfidsecuritysvc.model import BaseModel


class Sound(BaseModel):
    def __init__(self, id, name, last_update_timestamp=None, content=None):
        self.id = id
        self.name = name
        self.last_update_timestamp = last_update_timestamp
        self.content = content

    def to_json(self):
        """Override the base method to ensure that we don't show binary content everywhere"""
        cp = super().to_json()
        del cp['content']
        return cp

    def to_json_with_content(self):
        """This method must be explicitly called to get the content"""
        # In order to translate to JSON, this must be encoded first
        json = super().to_json()
        # Why not UTF-8? Because Base64 uses only ASCII characters
        # All ASCII characters are UTF-8
        json['content'] = base64.b64encode(self.content).decode('ascii')
        return json


def get(id):
    return __model(table.get(id))


def get_by_name(name):
    return __model(table.get_by_name(name))


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
    # All time in the database is stored as a string in ISO8601 format in UTC,
    # however, it doesn't store the offset/timezone in the string so we need to
    # add that information in
    t = datetime.fromisoformat(row['last_update_timestamp'])
    t = t.replace(tzinfo=timezone.utc)
    return Sound(row['id'], row['name'], t.isoformat(timespec='seconds'))
