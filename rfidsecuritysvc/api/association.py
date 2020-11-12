from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import association


def search():
    results = []
    for a in association.list():
        results.append(a.to_json())

    return results


def post(body):
    try:
        association.create(**body)
        return None, 201
    except exception.DuplicateAssociationError:
        return f'Object with media_id "{body["media_id"]}" and perm_name "{body["perm_name"]}" already exists.', 409


def delete(media_id, perm_name):
    try:
        return None, 200, {RECORD_COUNT_HEADER: association.delete(media_id, perm_name)}
    except exception.PermissionNotFoundError:
        # Becausse we're deleting by name, it's possible that the permission doesn't exist,
        # if this happens, return a 400 because the input is invalid
        return f'Permission "${perm_name}" does not exist.', 400
