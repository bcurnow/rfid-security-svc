import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import media_perm as model
from typing import Any

def get(id: int) -> tuple[dict | str, int]:
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search(media_id: str = None) -> list[dict]:
    results = []
    for m in model.list(media_id):
        results.append(m.to_json())

    return results


def post(body: dict[str, Any]) -> tuple[None | str, int]:
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateMediaPermError:
        return f'Object with media_id "{body["media_id"]}" and permission_id "{body["permission_id"]}" already exists.', 409
    except exception.MediaNotFoundError:
        return f'No media found with id "{body["media_id"]}".', 400
    except exception.PermissionNotFoundError:
        return f'No permission found with id "{body["permission_id"]}".', 400


def delete(id: int) -> tuple[None, int, dict]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(id))}


def put(id: int, body: dict[str, Any]) -> tuple[None, int, dict]:
    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(id, **body))}
    except exception.MediaPermNotFoundError:
        model.create(**body)
        return None, 201, {RECORD_COUNT_HEADER: '1'}
