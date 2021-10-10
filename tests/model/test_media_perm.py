import pytest

from unittest.mock import patch

import rfidsecuritysvc.model.media_perm as model
from rfidsecuritysvc.exception import MediaNotFoundError, PermissionNotFoundError
from rfidsecuritysvc.model.media_perm import MediaPerm
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.permission import Permission


def test_MediaPerm(open_door_media, open_door_permission):
    _assert_model(_model(1, open_door_media, open_door_permission), MediaPerm(1, open_door_media, open_door_permission))


@patch('rfidsecuritysvc.model.media_perm.table')
def test_get(table, media_perm_to_row):
    table.get.return_value = media_perm_to_row(_default())
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.media_perm.table')
def test_get_by_media_and_permission(table, media_perm_to_row):
    table.get_by_media_and_perm.return_value = media_perm_to_row(_default())
    assert model.get_by_media_and_perm('test', 1) == _default()
    table.get_by_media_and_perm.assert_called_once_with('test', 1)


@patch('rfidsecuritysvc.model.media_perm.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.media_perm.table')
def test_list(table, media_perm_to_row):
    table.list.return_value = [
        media_perm_to_row(_default()),
        media_perm_to_row(_default(2)),
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.media_perm.table')
def test_list_with_media_id(table, media_perm_to_row):
    table.list.return_value = [
        media_perm_to_row(_default()),
        media_perm_to_row(_default(2)),
    ]
    models = model.list('test')
    table.list.assert_called_once_with('test')
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.media_perm.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.media_perm.media')
@patch('rfidsecuritysvc.model.media_perm.permission')
@patch('rfidsecuritysvc.model.media_perm.table')
def test_create(table, permission, media):
    media.get.return_value = Media('test', 'test')
    permission.get.return_value = Permission(1, 'test')
    table.create.return_value = None
    assert model.create('test', 1) is None
    table.create.assert_called_once_with('test', 1)
    media.get.assert_called_once_with('test')
    permission.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.media_perm.media')
@patch('rfidsecuritysvc.model.media_perm.permission')
@patch('rfidsecuritysvc.model.media_perm.table')
def test_create_no_media(table, permission, media):
    media.get.return_value = None
    with pytest.raises(MediaNotFoundError):
        model.create('test', 1)
    media.get.assert_called_once_with('test')
    table.assert_not_called()
    permission.assert_not_called()


@patch('rfidsecuritysvc.model.media_perm.media')
@patch('rfidsecuritysvc.model.media_perm.permission')
@patch('rfidsecuritysvc.model.media_perm.table')
def test_create_no_permission(table, permission, media):
    media.get.return_value = Media('test', 'test')
    permission.get.return_value = None
    with pytest.raises(PermissionNotFoundError):
        model.create('test', 1)
    media.get.assert_called_once_with('test')
    permission.get.assert_called_once_with(1)
    table.assert_not_called()


@patch('rfidsecuritysvc.model.media_perm.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_with(1)


@patch('rfidsecuritysvc.model.media_perm.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update(1, 'test', 1) == 1
    table.update.assert_called_once_with(1, 'test', 1)


def _assert_model(expected, actual):
    assert expected.id == actual.id
    assert expected.media == actual.media
    assert expected.permission == actual.permission


def _default(index=1):
    m = Media(f'test media_id {index}', f'test media_name {index}', f'test media_desc {index}')
    p = Permission(f'test permission_id {index}', f'test permission_name {index}', f'test permission_desc {index}')
    return _model(index, m, p)


def _model(id, media, permission):
    return MediaPerm(id, media, permission)
