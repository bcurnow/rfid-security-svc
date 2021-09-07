import pytest
from unittest.mock import patch

from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.config import get, create, delete
from rfidsecuritysvc.exception import DuplicateConfigError as DuplicateError
from rfidsecuritysvc.exception import ConfigNotFoundError as NotFoundError
from rfidsecuritysvc.model.config import Config as Model

m = Model('key', 'value')


@patch('rfidsecuritysvc.cli.config.model')
def test_get(model, runner, assert_output):
    model.get.return_value = m
    result = runner.invoke(args=['config', 'get', m.key])
    assert_output(result, m.to_json())
    model.get.assert_called_once_with(m.key)


@patch('rfidsecuritysvc.cli.config.model')
def test_get_notfound(model, runner, assert_output):
    model.get.return_value = None
    result = runner.invoke(args=['config', 'get', m.key], color=True)
    assert_output(result, f'No record found with key "{m.key}".', 2, fg='red')
    model.get.assert_called_once_with(m.key)


def test_get_key_required():
    with pytest.raises(MissingParameter, match='Missing parameter: key'):
        get.make_context('config get', args=[])


@patch('rfidsecuritysvc.cli.config.model')
def test_list(model, runner, assert_output):
    m2 = Model('key2', 'value2')
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['config', 'list'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.config.model')
def test_create(model, runner, assert_output):
    model.create.return_value = None
    model.list.return_value = [m]
    result = runner.invoke(args=['config', 'create', m.key, m.value])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.key, m.value)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.config.model')
def test_create_duplicate(model, runner, assert_output):
    model.create.side_effect = DuplicateError
    result = runner.invoke(args=['config', 'create', m.key, m.value], color=True)
    assert_output(result, f'Record with key "{m.key}" already exists.', 2, fg='red')
    model.create.assert_called_once_with(m.key, m.value)


def test_create_key_required():
    with pytest.raises(MissingParameter, match='Missing parameter: key'):
        create.make_context('config create', args=[])


def test_create_value_required():
    with pytest.raises(MissingParameter, match='Missing parameter: value'):
        create.make_context('config create', args=[m.key])


@patch('rfidsecuritysvc.cli.config.model')
def test_delete(model, runner, assert_output):
    model.delete.return_value = 1
    result = runner.invoke(args=['config', 'delete', m.key], color=True)
    assert_output(result, '1 record(s) deleted.', bg='green', fg='black')
    model.delete.assert_called_once_with(m.key)


def test_delete_key_required():
    with pytest.raises(MissingParameter, match='Missing parameter: key'):
        delete.make_context('config delete', args=[])


@patch('rfidsecuritysvc.cli.config.model')
def test_update(model, runner, assert_output):
    model.update.return_value = 1
    model.list.return_value = [m]
    result = runner.invoke(args=['config', 'update', m.key, m.value], color=True)
    assert_output(result, 'Record updated.', bg='green', fg='black')
    model.update.assert_called_once_with(m.key, m.value)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.config.model')
def test_update_notfound(model, runner, assert_output):
    model.update.side_effect = NotFoundError
    result = runner.invoke(args=['config', 'update', m.key, m.value], color=True)
    assert_output(result, f'Record with key "{m.key}" does not exist.', 2, fg='red')
    model.update.assert_called_once_with(m.key, m.value)
