import pytest

from unittest.mock import patch

import rfidsecuritysvc.model.association as model
from rfidsecuritysvc.exception import PermissionNotFoundError, MediaNotFoundError, DuplicateMediaPermError, DuplicateAssociationError
from rfidsecuritysvc.model.association import Association
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.media_perm import MediaPerm
from rfidsecuritysvc.model.permission import Permission

def test_Association():
    _assert_model(_model('name', 'desc'), Association('name', 'desc'))

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
def test_get(permission, media_perm):
    expected = _default()
    permission.get_by_name.return_value = Permission(1, expected.perm_name)
    media_perm.get_by_media_and_perm.return_value = MediaPerm(1, expected.media_id, 1)
    assert model.get(expected.media_id, expected.perm_name) == expected
    permission.get_by_name.assert_called_once_with(expected.perm_name)
    media_perm.get_by_media_and_perm.assert_called_once_with(expected.media_id, 1)

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
def test_get_invalid_perm_name(permission, media_perm):
    permission.get_by_name.return_value = None
    with pytest.raises(PermissionNotFoundError):
        model.get('test', 'test_perm')
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.assert_not_called()

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
def test_get_notfound(permission, media_perm):
    permission.get_by_name.return_value = Permission(1, 'test_perm')
    media_perm.get_by_media_and_perm.return_value = None
    assert model.get('test', 'test_perm') == None
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 1)

@patch('rfidsecuritysvc.model.association.association')
def test_list(table):
    table.list.return_value = [
        _default().__dict__,
        _default(2).__dict__,
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]

@patch('rfidsecuritysvc.model.association.association')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
@patch('rfidsecuritysvc.model.association.media')
def test_create(media, permission, media_perm):
    media.get.return_value = Media('test', 'test')
    permission.get_by_name.return_value = Permission(1, 'test_perm')
    media_perm.create.return_value = None
    assert model.create('test', 'test_perm') == None
    media.get.assert_called_once_with('test')
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.create.assert_called_once_with('test', 1)

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
@patch('rfidsecuritysvc.model.association.media')
def test_create_invalid_media(media, permission, media_perm):
    media.get.return_value = None
    with pytest.raises(MediaNotFoundError):
        model.create('test', 'test_perm')
    media.get.assert_called_once_with('test')
    permission.assert_not_called()
    media_perm.assert_not_called()

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
@patch('rfidsecuritysvc.model.association.media')
def test_create_invalid_perm_name(media, permission, media_perm):
    media.get.return_value = Media('test', 'test')
    permission.get_by_name.return_value = None
    with pytest.raises(PermissionNotFoundError):
        model.create('test', 'test_perm')
    media.get.assert_called_once_with('test')
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.assert_not_called()

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
@patch('rfidsecuritysvc.model.association.media')
def test_create_duplicate_association(media, permission, media_perm):
    media.get.return_value = Media('test', 'test')
    permission.get_by_name.return_value = Permission(1, 'test_perm')
    media_perm.create.side_effect = DuplicateMediaPermError
    with pytest.raises(DuplicateAssociationError):
        model.create('test', 'test_perm')
    media.get.assert_called_once_with('test')
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.create.assert_called_once_with('test', 1)

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
def test_delete(permission, media_perm):
    permission.get_by_name.return_value = Permission(1, 'test_perm')
    media_perm.get_by_media_and_perm.return_value = MediaPerm(1, 'test', 1)
    media_perm.delete.return_value = 1
    assert model.delete('test', 'test_perm') == 1
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 1)
    media_perm.delete.assert_called_once_with(1)

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
def test_delete_invalid_perm_name(permission, media_perm):
    permission.get_by_name.return_value = None
    with pytest.raises(PermissionNotFoundError):
        model.delete('test', 'test_perm')
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.assert_not_called()

@patch('rfidsecuritysvc.model.association.media_perm')
@patch('rfidsecuritysvc.model.association.permission')
def test_delete_no_media_perm(permission, media_perm):
    permission.get_by_name.return_value = Permission(1, 'test_perm')
    media_perm.get_by_media_and_perm.return_value = None
    assert model.delete('test', 'test_perm') == 0
    permission.get_by_name.assert_called_once_with('test_perm')
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 1)

def _assert_model(expected, actual):
    assert expected.media_id == actual.media_id
    assert expected.perm_name == actual.perm_name

def _default(index=1):
    return _model(f'test media_id {index}', f'test perm_name {index}')

def _model(media_id, perm_name):
    return Association(media_id, perm_name)
