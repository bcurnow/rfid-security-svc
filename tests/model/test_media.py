from unittest.mock import patch

import rfidsecuritysvc.model.media as model
from rfidsecuritysvc.model.media import Media


def test_Media():
    _assert_model(_model('id', 'name', 'desc'), Media('id', 'name', 'desc'))


def test_Media_desc_optional():
    _assert_model(_model('id', 'name'), Media('id', 'name'))


@patch('rfidsecuritysvc.model.media.table')
def test_get(table):
    table.get.return_value = _default().__dict__
    assert model.get('test') == _default()
    table.get.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.media.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get('test') is None
    table.get.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.media.table')
def test_list(table):
    table.list.return_value = [
        _default().__dict__,
        _default(2).__dict__,
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.media.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.media.table')
def test_create(table):
    table.create.return_value = None
    assert model.create('test', 'test', 'test') is None
    table.create.assert_called_once_with('test', 'test', 'test')


@patch('rfidsecuritysvc.model.media.table')
def test_create_optional_desc(table):
    table.create.return_value = None
    assert model.create('test', 'test') is None
    table.create.assert_called_once_with('test', 'test', None)


@patch('rfidsecuritysvc.model.media.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete('test') == 1
    table.delete.asseret_called_with('test')


@patch('rfidsecuritysvc.model.media.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update('test', 'test', 'test') == 1
    table.update.assert_called_once_with('test', 'test', 'test')


@patch('rfidsecuritysvc.model.media.table')
def test_update_optional_desc(table):
    table.update.return_value = 1
    assert model.update('test', 'test') == 1
    table.update.assert_called_once_with('test', 'test', None)


def _assert_model(expected, actual):
    assert expected.id == actual.id
    assert expected.name == actual.name
    assert expected.desc == actual.desc


def _default(index=1):
    return _model(f'test media {index}', f'test media {index}', f'Media for testing ({index})')


def _model(id, name, desc=None):
    return Media(id, name, desc)
