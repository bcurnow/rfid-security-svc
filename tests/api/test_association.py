from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import association as api
from rfidsecuritysvc.exception import PermissionNotFoundError
from rfidsecuritysvc.exception import DuplicateAssociationError
from rfidsecuritysvc.exception import MediaNotFoundError
from rfidsecuritysvc.model.association import Association as Model

m = Model('test', 'Open Door')


@patch('rfidsecuritysvc.api.association.association')
def test_get(model):
    m2 = Model('test2', 'Close Door')
    model.by_media.return_value = [m, m2]
    assert api.get(m.media_id) == [m.to_json(), m2.to_json()]
    model.by_media.assert_called_once()


@patch('rfidsecuritysvc.api.association.association')
def test_search(model):
    m2 = Model('test2', 'Close Door')
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.association.association')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.association.association')
def test_post(model):
    model.create.return_value = None
    assert api.post(m.to_json()) == (None, 201)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.association.association')
def test_post_Duplicate(model):
    model.create.side_effect = DuplicateAssociationError
    assert api.post(m.to_json()) == (f'Object with media_id "{m.media_id}" and perm_name "{m.perm_name}" already exists.', 409)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.association.association')
def test_post_PermissionNotFound(model):
    model.create.side_effect = PermissionNotFoundError
    assert api.post(m.to_json()) == (f'Permission with name "{m.perm_name}" does not exist.', 400)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.association.association')
def test_post_MediaNotFound(model):
    model.create.side_effect = MediaNotFoundError
    assert api.post(m.to_json()) == (f'Media with id "{m.media_id}" does not exist.', 400)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.association.association')
def test_delete(model):
    model.delete.return_value = 1
    assert api.delete(m.media_id, m.perm_name) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.media_id, m.perm_name)


@patch('rfidsecuritysvc.api.association.association')
def test_delete_no_permission(model):
    model.delete.side_effect = PermissionNotFoundError
    assert api.delete(m.media_id, m.perm_name) == (f'Permission "${m.perm_name}" does not exist.', 400)
    model.delete.assert_called_once_with(m.media_id, m.perm_name)
