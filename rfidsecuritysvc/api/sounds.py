import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import sound as model
from typing import Any, Mapping

def get(id: int) -> dict | tuple[str, int]:
    m = model.get(id)
    if m:
        return m.to_json_with_content()

    return f'Object with id "{id}" does not exist.', 404


def search() -> list[dict[str, Any]]:
    return [m.to_json() for m in model.list()]


def post(body: Mapping[str, Any], content: Any) -> tuple[str | None, int]:
    if content is None or content.content_type != 'audio/wav':
        return 'audio/wav data is required', 415
    file_content = content.file.read()
    if content.size <= 0:
        return 'audio/wav data is required', 400
    name = body['name']

    try:
        model.create(name, file_content)
        return None, 201
    except exception.DuplicateSoundError:
        return f'Object with name "{name}" already exists.', 409


def delete(id: int) -> tuple[None, int, dict[str, str]]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(id))}


def put(id: int, body: Mapping[str, Any], content: Any) -> tuple[None, int, dict[str, str]]:
    if content is None or content.content_type != 'audio/wav':
        return 'audio/wav data is required', 415
    file_content = content.file.read()
    if content.size <= 0:
        return 'audio/wav data is required', 400
    name = body['name']

    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(id, name, file_content))}
    except exception.SoundNotFoundError:
        model.create(name, file_content)
        return None, 201, {RECORD_COUNT_HEADER: '1'}
