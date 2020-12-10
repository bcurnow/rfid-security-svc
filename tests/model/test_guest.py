from unittest.mock import patch

import rfidsecuritysvc.model.guest as model
from rfidsecuritysvc.model.guest import Guest


def test_Guest(assert_model):
    assert_model(_model(1, 'first', 'last'), Guest(1, 'first', 'last'))


@patch('rfidsecuritysvc.model.guest.table')
def test_get(table):
    table.get.return_value = _default().__dict__
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest.table')
def test_list(table):
    table.list.return_value = [
        _default().__dict__,
        _default(2).__dict__,
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.guest.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.guest.table')
def test_create(table):
    table.create.return_value = None
    assert model.create(1, 'first', 'last') is None
    table.create.assert_called_once_with(1, 'first', 'last')


@patch('rfidsecuritysvc.model.guest.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_with(1)


@patch('rfidsecuritysvc.model.guest.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update(1, 'first', 'last') == 1
    table.update.assert_called_once_with(1, 'first', 'last')


def _default(index=1):
    return _model(index, f'first {index}', f'last {index}')


def _model(id, first_name, last_name):
    return Guest(id, first_name, last_name)
