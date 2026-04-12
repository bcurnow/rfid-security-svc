import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import config as model
from typing import Any, Mapping

def get(key: str) -> dict | tuple[str, int]:
    m = model.get(key)
    if m:
        return m.to_json()
    return f'Object with key "{key}" does not exist.', 404


def search() -> list[dict[str, Any]]:
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results


def post(body: Mapping[str, Any]) -> tuple[None | str, int]:
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateConfigError:
        return f'Object with key "{body["key"]}" already exists.', 409


def delete(key: str) -> tuple[None, int, dict[str, str]]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(key))}


def put(key: str, body: Mapping[str, Any]) -> tuple[None, int, dict[str, str]]:
    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(key, body['value']))}
    except exception.ConfigNotFoundError:
        model.create(key, body['value'])
        return None, 201, {RECORD_COUNT_HEADER: '1'}
