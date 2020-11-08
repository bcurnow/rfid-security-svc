import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import media_perm as model

def get(media_id, perm_id):
    m = model.get_by_media_and_perm(media_id, perm_id)
    if m: return m.to_json()
    return f'Object with media_id "{media_id}" and perm_id "{perm_id}" does not exist.', 404

def search():
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results

def post(body):
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateMediaPermError as e:
        return f'Object with media_id "{body["media_id"]}" and perm_id "{body["perm_id"]}" already exists.', 409
    except exception.MediaNotFoundError:
        return f'No media found with id "{body["media_id"]}".', 400
    except exception.PermissionNotFoundError:
        return f'No permission found with id "{body["perm_id"]}".', 400

def delete(media_id, perm_id):
    return None, 200, {RECORD_COUNT_HEADER: model.delete_by_media_and_perm(media_id, perm_id)}

def put(media_id, perm_id):
    try:
        # Since there are no additional fields beyond media_id and perm_id, assume this is a create
        model.create(media_id, perm_id)
        return None, 201, {RECORD_COUNT_HEADER: 1}
    except exception.DuplicateMediaPermError:
        # This already exists so simply return a 200 because there's nothing else to update
        return None, 200, {RECORD_COUNT_HEADER: 0}
