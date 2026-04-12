import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import media as model
from typing import Any

def get(id: str) -> tuple[dict | str, int]:
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search(exclude_associated: bool = False) -> list[dict]:
    results = []
    for m in model.list(exclude_associated):
        results.append(m.to_json())

    return results


def post(body: dict[str, Any]) -> tuple[None | str, int]:
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateMediaError:
        return f'Object with id "{body["id"]}" or name "{body["name"]}" already exists.', 409


def delete(id: str) -> tuple[None, int, dict]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(id))}


def put(id: str, body: dict[str, Any]) -> tuple[None, int, dict]:
    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(id, **body))}
    except exception.MediaNotFoundError:
        model.create(id, **body)
        return None, 201, {RECORD_COUNT_HEADER: '1'}
