import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import media as model


def get(id):
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search(excludeAssociated=False):
    results = []
    for m in model.list(excludeAssociated):
        results.append(m.to_json())

    return results


def post(body):
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateMediaError:
        return f'Object with id "{body["id"]}" or name "{body["name"]}" already exists.', 409


def delete(id):
    return None, 200, {RECORD_COUNT_HEADER: model.delete(id)}


def put(id, body):
    try:
        return None, 200, {RECORD_COUNT_HEADER: model.update(id, **body)}
    except exception.MediaNotFoundError:
        model.create(id, **body)
        return None, 201, {RECORD_COUNT_HEADER: 1}
