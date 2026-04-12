import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import guest_media as model
from typing import Any

def get(id: int) -> tuple[dict | str, int]:
    m = model.get(id)
    if m:
        return m.to_json()
    return f'Object with id "{id}" does not exist.', 404


def search(guest_id: int = None) -> list[dict]:
    results = []
    for m in model.list(guest_id):
        results.append(m.to_json())

    return results


def post(body: dict[str, Any]) -> tuple[None | str, int]:
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateGuestMediaError:
        return f'Media with media_id "{body["media_id"]} is already associated with a guest.', 409
    except exception.GuestNotFoundError:
        return f'No guest found with id "{body["guest_id"]}".', 400
    except exception.MediaNotFoundError:
        return f'No media found with id "{body["media_id"]}".', 400
    except exception.SoundNotFoundError:
        return f'No sound found with id "{body["sound"]}".', 400


def delete(id: int) -> tuple[None, int, dict]:
    return None, 200, {RECORD_COUNT_HEADER: str(model.delete(id))}


def put(id: int, body: dict[str, Any]) -> tuple[None | str, int, dict]:
    try:
        return None, 200, {RECORD_COUNT_HEADER: str(model.update(id, **body))}
    except exception.GuestNotFoundError:
        return f'No guest found with id "{body["guest_id"]}".', 400
    except exception.MediaNotFoundError:
        return f'No media found with id "{body["media_id"]}".', 400
    except exception.SoundNotFoundError:
        return f'No sound found with id "{body["sound"]}".', 400
    except exception.GuestMediaNotFoundError:
        # In theory, this should never throw and exception but, in case it ever does...
        try:
            model.create(**body)
            return None, 201, {RECORD_COUNT_HEADER: '1'}
        except exception.DuplicateGuestMediaError:
            return f'Object with guest_id "{body["guest_id"]} and media_id "{body["media_id"]}" already exists.', 409
        except exception.GuestNotFoundError:
            return f'No guest found with id "{body["guest_id"]}".', 400
        except exception.MediaNotFoundError:
            return f'No media found with id "{body["media_id"]}".', 400
        except exception.SoundNotFoundError:
            return f'No sound found with id "{body["sound"]}".', 400
