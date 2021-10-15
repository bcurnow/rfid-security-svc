import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import guest as model


def get(id):
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search():
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results


def post(body):
    try:
        model.create(**body)
        return None, 201
    except exception.SoundNotFoundError:
        return f'Sound with id "{body["sound"]}" does not exist.', 400
    except exception.DuplicateGuestError:
        return f'Object with first_name "{body["first_name"]}" and last_name "{body["last_name"]}" already exists.', 409


def delete(id):
    return None, 200, {RECORD_COUNT_HEADER: model.delete(id)}


def put(id, body):
    try:
        return None, 200, {RECORD_COUNT_HEADER: model.update(id, **body)}
    except exception.SoundNotFoundError:
        return f'Sound with id "{body["sound"]}" does not exist.', 400
    except exception.GuestNotFoundError:
        try:
            model.create(**body)
            return None, 201, {RECORD_COUNT_HEADER: 1}
        except exception.SoundNotFoundError:
            return f'Sound with id "{body["sound"]}" does not exist.', 400
