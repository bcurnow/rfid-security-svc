import pytest
from unittest.mock import patch

from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.media_perm import get, create, delete
from rfidsecuritysvc.exception import DuplicateMediaPermError as DuplicateError
from rfidsecuritysvc.exception import MediaPermNotFoundError as NotFoundError
from rfidsecuritysvc.exception import MediaNotFoundError
from rfidsecuritysvc.exception import PermissionNotFoundError
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.media_perm import MediaPerm as Model
from rfidsecuritysvc.model.permission import Permission


media = Media('media_id', 'media_name', 'media_desc')
permission = Permission(2, 'permission_name', 'permission_desc')
m = Model(1, media, permission)


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
    assert_output(result, f'No record found with id "{m.id}".', 2, fg='red')
    model.get.assert_called_once_with(m.id)


def test_get_id_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: id'):
        get.make_context('media-perm get', args=[])


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_list(model, runner, assert_output):
    media2 = Media('media_id2', 'media_name2', 'media_desc2')
    permission2 = Permission(4, 'permission_name2', 'permission_desc2')
    m2 = Model(3, media2, permission2)
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['media-perm', 'list'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_list_with_media_id(model, runner, assert_output):
    media2 = Media('media_id2', 'media_name2', 'media_desc2')
    permission2 = Permission(4, 'permission_name2', 'permission_desc2')
    m2 = Model(3, media2, permission2)
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['media-perm', 'list', 'test'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once_with('test')


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create(model, runner, assert_output):
    model.create.return_value = None
    model.list.return_value = [m]
    result = runner.invoke(args=['media-perm', 'create', m.media.id, str(m.permission.id)])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.media.id, m.permission.id)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create_duplicate(model, runner, assert_output):
    model.create.side_effect = DuplicateError
    result = runner.invoke(args=['media-perm', 'create', m.media.id, str(m.permission.id)], color=True)
    assert_output(result, f'Record with media_id "{m.media.id}" and permission_id "{m.permission.id}" already exists.', 2, fg='red')
    model.create.assert_called_once_with(m.media.id, m.permission.id)


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create_media_notfound(model, runner, assert_output):
    model.create.side_effect = MediaNotFoundError
    result = runner.invoke(args=['media-perm', 'create', m.media.id, str(m.permission.id)], color=True)
    assert_output(result, f'No media found with id "{m.media.id}".', 2, fg='red')
    model.create.assert_called_once_with(m.media.id, m.permission.id)


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_create_permission_notfound(model, runner, assert_output):
    model.create.side_effect = PermissionNotFoundError
    result = runner.invoke(args=['media-perm', 'create', m.media.id, str(m.permission.id)], color=True)
    assert_output(result, f'No permission found with id "{m.permission.id}".', 2, fg='red')
    model.create.assert_called_once_with(m.media.id, m.permission.id)


def test_create_media_id_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: media_id'):
        create.make_context('media-perm create', args=[])


def test_create_permission_id_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: permission_id'):
        create.make_context('media-perm create', args=[m.media.id])


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_delete(model, runner, assert_output):
    model.delete.return_value = 1
    result = runner.invoke(args=['media-perm', 'delete', str(m.id)], color=True)
    assert_output(result, '1 record(s) deleted.', bg='green', fg='black')
    model.delete.assert_called_once_with(m.id)


def test_delete_id_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: id'):
        delete.make_context('media-perm delete', args=[])


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_update(model, runner, assert_output):
    model.update.return_value = 1
    model.list.return_value = [m]
    result = runner.invoke(args=['media-perm', 'update', str(m.id), m.media.id, str(m.permission.id)], color=True)
    assert_output(result, 'Record updated.', bg='green', fg='black')
    model.update.assert_called_once_with(m.id, m.media.id, m.permission.id)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.media_perm.model')
def test_update_notfound(model, runner, assert_output):
    model.update.side_effect = NotFoundError
    result = runner.invoke(args=['media-perm', 'update', str(m.id), m.media.id, str(m.permission.id)], color=True)
    assert_output(result, f'Record with id "{m.id}", media_id "{m.media.id}" and permission_id "{m.permission.id}" does not exist.', 2, fg='red')
    model.update.assert_called_once_with(m.id, m.media.id, m.permission.id)
