from rfidsecuritysvc.db import guest as table
from rfidsecuritysvc.model import BaseModel


class Guest(BaseModel):
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


def get(id):
    return __model(table.get(id))


def list():
    result = []
    for row in table.list():
        result.append(__model(row))

    return result


def create(id, first_name, last_name):
    return table.create(id, first_name, last_name)


def delete(id):
    return table.delete(id)


def update(id, first_name, last_name):
    return table.update(id, first_name, last_name)


def __model(row):
    if not row:
        return
    return Guest(row['id'], row['first_name'], row['last_name'])
