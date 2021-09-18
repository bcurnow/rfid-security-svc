import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import sound as model


def get(name):
    m = model.get(name)
    if m:
        return m.to_json()
    return f'Object with name "{name}" does not exist.', 404


def search():
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results


def post(name, body):
    try:
        model.create(name, body)
        return None, 201
    except exception.DuplicateSoundError:
        return f'Object with name "{name}" already exists.', 409


def delete(name):
    return None, 200, {RECORD_COUNT_HEADER: model.delete(name)}


def put(id, name, body):
    try:
        return None, 200, {RECORD_COUNT_HEADER: model.update(id, name, body)}
    except exception.SoundNotFoundError:
        model.create(id, name, body)
        return None, 201, {RECORD_COUNT_HEADER: 1}
