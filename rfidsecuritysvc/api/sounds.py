from flask import request

import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model import sound as model


def get(name):
    m = model.get(name)
    if m:
        return m.to_json_with_content()
    return f'Object with name "{name}" does not exist.', 404


def search():
    results = []
    for m in model.list():
        results.append(m.to_json())

    return results


def post():
    name = request.form['name']
    content = request.files['content']
    if content.content_type != 'audio/wav':
        return 'audio/wav data is required', 415
    file_content = content.read()
    if _content_length(content, file_content) <= 0:
        return 'audio/wav data is required', 400

    try:
        model.create(name, file_content)
        return None, 201
    except exception.DuplicateSoundError:
        return f'Object with name "{name}" already exists.', 409


def delete(name):
    return None, 200, {RECORD_COUNT_HEADER: model.delete(name)}


def put(id):
    name = request.form['name']
    content = request.files['content']
    if content.content_type != 'audio/wav':
        return 'audio/wav data is required', 415
    file_content = content.read()
    if _content_length(content, file_content) <= 0:
        return 'audio/wav data is required', 400

    try:
        return None, 200, {RECORD_COUNT_HEADER: model.update(id, name, file_content)}
    except exception.SoundNotFoundError:
        model.create(name, file_content)
        return None, 201, {RECORD_COUNT_HEADER: 1}


def _content_length(file, file_content):
    # Determine the actual length of the content.
    # Some clients (e.g flask test_request_context) don't provide the
    # content_length but do provide the content
    if file.content_length <= 0:
        return len(file_content)
    else:
        return file.content_length
