from unittest.mock import patch

import rfidsecuritysvc.model.sound as model
from rfidsecuritysvc.model.sound import Sound


def test_Sound():
    _assert_model(_model('id', 'name', 'binary content'), Sound('id', 'name', 'binary content'))
    _assert_model(_model('id', 'name'), Sound('id', 'name'))


@patch('rfidsecuritysvc.model.sound.table')
def test_get(table):
    table.get.return_value = _default().__dict__
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.sound.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.sound.table')
def test_list(table):
    table.list.return_value = [
        _default().__dict__,
        _default(2).__dict__,
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.sound.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.sound.table')
def test_create(table):
    table.create.return_value = None
    assert model.create('test', 'binary content') is None
    table.create.assert_called_once_with('test', 'binary content')


@patch('rfidsecuritysvc.model.sound.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.sound.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update(1, 'test') == 1
    table.update.assert_called_once_with(1, 'test')


def _assert_model(expected, actual):
    assert expected.id == actual.id
    assert expected.name == actual.name


def _default(index=1):
    return _model(f'test id {index}', f'test name {index}')


def _model(id, name, content=None):
    return Sound(id, name, content)