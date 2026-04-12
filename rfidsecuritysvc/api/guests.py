import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import guest as model
from typing import Any

def get(id: int) -> tuple[dict | str, int]:
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search() -> list[dict]:
    return [m.to_json() for m in model.list()]


def post(body: dict[str, Any]) -> tuple[dict | str, int]:
    try:
        m = model.create(**body)
        if m:
            return m.to_json(), 201
        return f'Unable to retrieve newly inserted object.', 404
    except exception.SoundNotFoundError:
        return f'Sound with id "{body["sound"]}" does not exist.', 400
    except exception.DuplicateGuestError:
        return f'Object with first_name "{body["first_name"]}" and last_name "{body["last_name"]}" already exists.', 409


def delete(id: int) -> tuple[None, int, dict]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(id))}


def put(id: int, body: dict[str, Any]) -> tuple[None | str, int, dict]:
    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(id, **body))}
    except exception.SoundNotFoundError:
        return f'Sound with id "{body["sound"]}" does not exist.', 400
    except exception.GuestNotFoundError:
        try:
            model.create(**body)
            return None, 201, {RECORD_COUNT_HEADER: '1'}
        except exception.SoundNotFoundError:
            return f'Sound with id "{body["sound"]}" does not exist.', 400
