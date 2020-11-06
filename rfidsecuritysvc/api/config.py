import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import config as model

def get(key):
    m = model.get(key)
    if m: return m.to_json()
    return f'Object with key "{key}" does not exist.', 404

def search():
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results

def post(body):
    try:
        model.create(**body)
        return None, 201
    except exception.DuplicateConfigError:
        return f'Object with key "{body["key"]}" already exists.', 409

def delete(key):
    model.delete(key)
    return None, 200 

def put(key, body):
    try:
        model.update(key, body["value"])
        return None, 200
    except exception.ConfigNotFoundError:
        model.create(key, body["value"])
        return None, 201

