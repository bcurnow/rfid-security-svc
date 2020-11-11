import pytest
from unittest.mock import patch

import click
from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.media import get, list, create, delete, update
from rfidsecuritysvc.exception import DuplicateMediaError as DuplicateError
from rfidsecuritysvc.exception import MediaNotFoundError as NotFoundError
from rfidsecuritysvc.exception import MediaNotFoundError
from rfidsecuritysvc.exception import PermissionNotFoundError
from rfidsecuritysvc.model.media import Media as Model

m = Model('id', 'name', 'desc')

@patch('rfidsecuritysvc.cli.media.model')
def test_get(model, runner, assert_output):
    model.get.return_value = m
    result = runner.invoke(args=['media', 'get', m.id])
    assert_output(result, m.to_json())
    model.get.assert_called_once_with(m.id)

@patch('rfidsecuritysvc.cli.media.model')
def test_get_notfound(model, runner, assert_output):
    model.get.return_value = None
    result = runner.invoke(args=['media', 'get', m.id], color=True)
    assert_output(result, f'No record found with id "{m.id}".', fg='red')
    model.get.assert_called_once_with(m.id)

def test_get_id_required():
    with pytest.raises(MissingParameter):
        get.make_context('media get', args=[])

@patch('rfidsecuritysvc.cli.media.model')
def test_list(model, runner, assert_output):
    m2 = Model('id2', 'name2', 'desc2')
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['media', 'list'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once()

@patch('rfidsecuritysvc.cli.media.model')
def test_create(model, runner, assert_output):
    model.create.return_value = None
    model.list.return_value = [m]
    result = runner.invoke(args=['media', 'create', m.id, m.name, m.desc])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.id, m.name, m.desc)
    model.list.assert_called_once()

@patch('rfidsecuritysvc.cli.media.model')
def test_create_duplicate(model, runner, assert_output):
    model.create.side_effect = DuplicateError
    result = runner.invoke(args=['media', 'create', m.id, m.name, m.desc], color=True)
    print(result)
    print(result.output)
    assert_output(result, f'Record with id "{m.id}" or name "{m.name}" already exists.', fg='red')
    model.create.assert_called_once_with(m.id, m.name, m.desc)

def test_create_id_required():
    with pytest.raises(MissingParameter):
        create.make_context('media create', args=[])

def test_create_name_required():
    with pytest.raises(MissingParameter):
        create.make_context('media create', args=[m.id])

def test_create_desc_optional():
    create.make_context('media create', args=[m.id, m.name])


@patch('rfidsecuritysvc.cli.media.model')
def test_delete(model, runner, assert_output):
    model.delete.return_value = 1
    result = runner.invoke(args=['media', 'delete', m.id], color=True)
    assert_output(result, f'1 record(s) deleted.', bg='green', fg='black')
    model.delete.assert_called_once_with(m.id)

def test_delete_id_required():
    with pytest.raises(MissingParameter):
        delete.make_context('media delete', args=[])

@patch('rfidsecuritysvc.cli.media.model')
def test_update(model, runner, assert_output):
    model.update.return_value = 1
    model.list.return_value = [m]
    result = runner.invoke(args=['media', 'update', m.id, m.name, m.desc], color=True)
    assert_output(result, f'Record updated.', bg='green', fg='black')
    model.update.assert_called_once_with(m.id, m.name, m.desc)
    model.list.assert_called_once()

@patch('rfidsecuritysvc.cli.media.model')
def test_update_notfound(model, runner, assert_output):
    model.update.side_effect = NotFoundError
    result = runner.invoke(args=['media', 'update', m.id, m.name, m.desc], color=True)
    assert_output(result, f'Record with id "{m.id}" does not exist.', fg='red')
    model.update.assert_called_once_with(m.id, m.name, m.desc)
