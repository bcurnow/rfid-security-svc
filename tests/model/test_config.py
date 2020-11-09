from unittest.mock import patch

import rfidsecuritysvc.model.config as model
from rfidsecuritysvc.model.config import Config

def test_Config():
    _assert_model(_model('key', 'value'), Config('key', 'value'))

@patch('rfidsecuritysvc.model.config.table')
def test_get(table):
    table.get.return_value = _default().__dict__
    assert model.get('test') == _default()
    table.get.assert_called_once_with('test')

@patch('rfidsecuritysvc.model.config.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get('test') == None
    table.get.assert_called_once_with('test')

@patch('rfidsecuritysvc.model.config.table')
def test_list(table):
    table.list.return_value = [
        _default().__dict__,
        _default(2).__dict__,
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]

@patch('rfidsecuritysvc.model.config.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []

@patch('rfidsecuritysvc.model.config.table')
def test_create(table):
    table.create.return_value = None
    assert model.create('test', 'test') == None
    table.create.assert_called_once_with('test', 'test')

@patch('rfidsecuritysvc.model.config.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete('test') == 1
    table.delete.asseret_called_with('test')

@patch('rfidsecuritysvc.model.config.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update('test', 'test') == 1
    table.update.assert_called_once_with('test', 'test')

def _assert_model(expected, actual):
    assert expected.key == actual.key
    assert expected.value == actual.value

def _default(index=1):
    return _model(f'test key {index}', f'test value {index}')

def _model(key, value):
    return Config(key, value)
