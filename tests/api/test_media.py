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
    model.list.assert_called_once_with(False)


@patch('rfidsecuritysvc.api.media.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once_with(False)


@patch('rfidsecuritysvc.api.media.model')
def test_search_exclude_associated(model):
    m2 = Model('test2', 'name2', 'desc2')
    model.list.return_value = [m, m2]
    assert api.search(True) == [m.to_json(), m2.to_json()]
    model.list.assert_called_once_with(True)


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
    assert api.put(m.id, m.test_update()) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **m.test_update())


@patch('rfidsecuritysvc.api.media.model')
def test_put_does_not_exist(model):
    model.update.side_effect = NotFoundError
    assert api.put(m.id, m.test_update()) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **m.test_update())
    model.create.assert_called_once_with(m.id, **m.test_update())
