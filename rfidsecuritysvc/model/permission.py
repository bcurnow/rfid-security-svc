from rfidsecuritysvc.db import permission as table
from rfidsecuritysvc.model import BaseModel


class Permission(BaseModel):
    def __init__(self, id, name, desc=None):
        self.id = id
        self.name = name
        self.desc = desc


    def _read_only_keys(self):
        return ['id']


def get(id):
    return __model(table.get(id))


def get_by_name(name):
    return __model(table.get_by_name(name))


def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result


def create(name, desc=None):
    return table.create(name, desc)


def delete(id):
    return table.delete(id)


def delete_by_name(name):
    return table.delete_by_name(name)


def update(id, name, desc=None):
    return table.update(id, name, desc)


def update_by_name(name, desc=None):
    return table.update_by_name(name, desc)


def __model(row):
    if not row:
        return
    return Permission(row['id'], row['name'], row['desc'])
