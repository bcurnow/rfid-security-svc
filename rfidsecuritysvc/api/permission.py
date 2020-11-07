import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import permission as model

def get(name):
    m = model.get_by_name(name)
    if m: return m.to_json()
    return f'Object with name "{name}" does not exist.', 404

def search():
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results

def post(body):
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicatePermissionError:
        return f'Object with name "{body["name"]}" already exists.', 409

def delete(name):
    return None, 200, {RECORD_COUNT_HEADER: model.delete_by_name(name)}

def put(name, body):
    try:
        model.update_by_name(name, body['desc'])
        return None, 200
    except exception.PermissionNotFoundError:
        model.create(name, body['desc'])
        return None, 201
