from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import configs as api
from rfidsecuritysvc.exception import DuplicateConfigError as DuplicateError
from rfidsecuritysvc.exception import ConfigNotFoundError as NotFoundError
from rfidsecuritysvc.model.config import Config as Model

m = Model('key', 'value')


@patch('rfidsecuritysvc.api.configs.model')
def test_get(model):
    model.get.return_value = m
    assert api.get(m.key) == m.to_json()
    model.get.assert_called_once_with(m.key)


@patch('rfidsecuritysvc.api.configs.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get(m.key) == (f'Object with key "{m.key}" does not exist.', 404)
    model.get.assert_called_once_with(m.key)


@patch('rfidsecuritysvc.api.configs.model')
def test_search(model):
    m2 = Model('key2', 'value2')
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.configs.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.configs.model')
def test_post(model):
    model.create.return_value = None
    assert api.post(m.to_json()) == (None, 201)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.configs.model')
def test_post_Duplicate(model):
    model.create.side_effect = DuplicateError
    assert api.post(m.to_json()) == (f'Object with key "{m.key}" already exists.', 409)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.configs.model')
def test_delete(model):
    model.delete.return_value = 1
    assert api.delete(m.key) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.key)


@patch('rfidsecuritysvc.api.configs.model')
def test_put(model):
    model.update.return_value = 1
    assert api.put(m.key, m.to_json()) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.key, m.value)


@patch('rfidsecuritysvc.api.configs.model')
def test_put_already_exists(model):
    model.update.side_effect = NotFoundError
    assert api.put(m.key, m.to_json()) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.key, m.value)
    model.create.assert_called_once_with(m.key, m.value)
