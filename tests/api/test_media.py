from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import media as api
from rfidsecuritysvc.exception import DuplicateMediaError as DuplicateError
from rfidsecuritysvc.exception import MediaNotFoundError as NotFoundError
from rfidsecuritysvc.model.media import Media as Model

m = Model('test', 'name', 'desc')


@patch('rfidsecuritysvc.api.media.model')
def test_get(model):
    model.get.return_value = m
    assert api.get(m.id) == m.to_json()
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.media.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get(m.id) == (f'Object with id "{m.id}" does not exist.', 404)
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.media.model')
def test_search(model):
    m2 = Model('test2', 'name2', 'desc2')
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.media.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.media.model')
def test_post(model):
    model.create.return_value = None
    assert api.post(m.to_json()) == (None, 201)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.media.model')
def test_post_Duplicate(model):
    model.create.side_effect = DuplicateError
    assert api.post(m.to_json()) == (f'Object with id "{m.id}" or name "{m.name}" already exists.', 409)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.media.model')
def test_delete(model):
    model.delete.return_value = 1
    assert api.delete(m.id) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.media.model')
def test_put(model):
    model.update.return_value = 1
    assert api.put(m.id, _update(m)) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **_update(m))


@patch('rfidsecuritysvc.api.media.model')
def test_put_does_not_exist(model):
    model.update.side_effect = NotFoundError
    assert api.put(m.id, _update(m)) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **_update(m))
    model.create.assert_called_once_with(m.id, **_update(m))


def _update(m):
    """
    This is only needed for the Media object because it's the only one that has a non-generated id.
    It can't be marked read-only in the schema because it has to be allowed in the post/create flow.
    So, we need to drop the ID when doing an update.
    """
    json = m.to_json().copy()
    del json['id']
    return json
