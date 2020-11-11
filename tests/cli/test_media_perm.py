import pytest
from unittest.mock import patch

import click
from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.media_perm import get, list, create, delete, update
from rfidsecuritysvc.exception import DuplicateMediaPermError as DuplicateError
from rfidsecuritysvc.exception import MediaPermNotFoundError as NotFoundError
from rfidsecuritysvc.exception import MediaNotFoundError
from rfidsecuritysvc.exception import PermissionNotFoundError
from rfidsecuritysvc.model.media_perm import MediaPerm as Model

m = Model(1, 'media_id', 2)

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_get(model, runner, assert_output):
    model.get.return_value = m
    result = runner.invoke(args=['media-perm', 'get', str(m.id)])
    assert_output(result, m.to_json())
    model.get.assert_called_once_with(m.id)

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_get_notfound(model, runner, assert_output):
    model.get.return_value = None
    result = runner.invoke(args=['media-perm', 'get', str(m.id)], color=True)
    assert_output(result, f'No record found with id "{m.id}".', fg='red')
    model.get.assert_called_once_with(m.id)

def test_get_id_required():
    with pytest.raises(MissingParameter):
        get.make_context('media-perm get', args=[])

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_list(model, runner, assert_output):
    m2 = Model(3, 'media_id2', 4)
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['media-perm', 'list'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once()

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create(model, runner, assert_output):
    model.create.return_value = None
    model.list.return_value = [m]
    result = runner.invoke(args=['media-perm', 'create', m.media_id, str(m.perm_id)])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.media_id, m.perm_id)
    model.list.assert_called_once()

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create_duplicate(model, runner, assert_output):
    model.create.side_effect = DuplicateError
    result = runner.invoke(args=['media-perm', 'create', m.media_id, str(m.perm_id)], color=True)
    print(result)
    print(result.output)
    assert_output(result, f'Record with media_id "{m.media_id}" and perm_id "{m.perm_id}" already exists.', fg='red')
    model.create.assert_called_once_with(m.media_id, m.perm_id)

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create_media_notfound(model, runner, assert_output):
    model.create.side_effect = MediaNotFoundError
    result = runner.invoke(args=['media-perm', 'create', m.media_id, str(m.perm_id)], color=True)
    assert_output(result, f'No media found with id "{m.media_id}".', fg='red')
    model.create.assert_called_once_with(m.media_id, m.perm_id)

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create_media_notfound(model, runner, assert_output):
    model.create.side_effect = PermissionNotFoundError
    result = runner.invoke(args=['media-perm', 'create', m.media_id, str(m.perm_id)], color=True)
    assert_output(result, f'No permission found with id "{m.perm_id}".', fg='red')
    model.create.assert_called_once_with(m.media_id, m.perm_id)

def test_create_media_id_required():
    with pytest.raises(MissingParameter):
        create.make_context('media-perm create', args=[])

def test_create_perm_id_required():
    with pytest.raises(MissingParameter):
        create.make_context('media-perm create', args=[m.media_id])

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_delete(model, runner, assert_output):
    model.delete.return_value = 1
    result = runner.invoke(args=['media-perm', 'delete', str(m.id)], color=True)
    assert_output(result, f'1 record(s) deleted.', bg='green', fg='black')
    model.delete.assert_called_once_with(m.id)

def test_delete_id_required():
    with pytest.raises(MissingParameter):
        delete.make_context('media-perm delete', args=[])

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_update(model, runner, assert_output):
    model.update.return_value = 1
    model.list.return_value = [m]
    result = runner.invoke(args=['media-perm', 'update', str(m.id), m.media_id, str(m.perm_id)], color=True)
    assert_output(result, f'Record updated.', bg='green', fg='black')
    model.update.assert_called_once_with(m.id, m.media_id, m.perm_id)
    model.list.assert_called_once()

@patch('rfidsecuritysvc.cli.media_perm.model')
def test_update_notfound(model, runner, assert_output):
    model.update.side_effect = NotFoundError
    result = runner.invoke(args=['media-perm', 'update', str(m.id), m.media_id, str(m.perm_id)], color=True)
    assert_output(result, f'Record with id "{m.id}", media_id "{m.media_id}" and perm_id "{m.perm_id}" does not exist.', fg='red')
    model.update.assert_called_once_with(m.id, m.media_id, m.perm_id)
