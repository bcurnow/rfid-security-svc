from unittest.mock import patch

import rfidsecuritysvc.model.permission as model
from rfidsecuritysvc.model.permission import Permission


def test_Permission():
    _assert_model(_model(1, 'name', 'desc'), Permission(1, 'name', 'desc'))


def test_Permission_desc_optional():
    _assert_model(_model(1, 'name'), Permission(1, 'name'))


@patch('rfidsecuritysvc.model.permission.table')
def test_get(table):
    table.get.return_value = _default().__dict__
    assert model.get('test') == _default()
    table.get.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.permission.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get('test') is None
    table.get.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.permission.table')
def test_get_by_name(table):
    table.get_by_name.return_value = _default().__dict__
    assert model.get_by_name('test') == _default()
    table.get_by_name.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.permission.table')
def test_list(table):
    table.list.return_value = [
        _default().__dict__,
        _default(2).__dict__,
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.permission.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.permission.table')
def test_create(table):
    table.create.return_value = None
    assert model.create('test', 'test') is None
    table.create.assert_called_once_with('test', 'test')


@patch('rfidsecuritysvc.model.permission.table')
def test_create_optional_desc(table):
    table.create.return_value = None
    assert model.create('test') is None
    table.create.assert_called_once_with('test', None)


@patch('rfidsecuritysvc.model.permission.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_with(1)


@patch('rfidsecuritysvc.model.permission.table')
def test_delete_by_name(table):
    table.delete_by_name.return_value = 1
    assert model.delete_by_name('test') == 1
    table.delete_by_name.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.permission.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update(1, 'test', 'test') == 1
    table.update.assert_called_once_with(1, 'test', 'test')


@patch('rfidsecuritysvc.model.permission.table')
def test_update_optional_desc(table):
    table.update.return_value = 1
    assert model.update(1, 'test') == 1
    table.update.assert_called_once_with(1, 'test', None)


@patch('rfidsecuritysvc.model.permission.table')
def test_update_by_name(table):
    table.update_by_name.return_value = 1
    assert model.update_by_name('test', 'test') == 1
    table.update_by_name.assert_called_once_with('test', 'test')


@patch('rfidsecuritysvc.model.permission.table')
def test_update_by_name_optional_desc(table):
    table.update_by_name.return_value = 1
    assert model.update_by_name('test') == 1
    table.update_by_name.assert_called_once_with('test', None)


def _assert_model(expected, actual):
    assert expected.id == actual.id
    assert expected.name == actual.name
    assert expected.desc == actual.desc


def _default(index=1):
    return _model(index, f'test permission {index}', f'Permission for testing ({index})')


def _model(id, name, desc=None):
    return Permission(id, name, desc)
