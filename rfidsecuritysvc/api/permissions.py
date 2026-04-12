import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import permission as model
from typing import Any

def get(id: int) -> tuple[dict | str, int]:
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search() -> list[dict]:
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results


def post(body: dict[str, Any]) -> tuple[None | str, int]:
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicatePermissionError:
        return f'Object with name "{body["name"]}" already exists.', 409


def delete(id: int) -> tuple[None, int, dict]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(id))}


def put(id: int, body: dict[str, Any]) -> tuple[None, int, dict]:
    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(id, **body))}
    except exception.PermissionNotFoundError:
        model.create(**body)
        return None, 201, {RECORD_COUNT_HEADER: '1'}
