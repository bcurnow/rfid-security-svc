from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import media_perms as api
from rfidsecuritysvc.exception import DuplicateMediaPermError as DuplicateError
from rfidsecuritysvc.exception import MediaNotFoundError
from rfidsecuritysvc.exception import MediaPermNotFoundError
from rfidsecuritysvc.exception import PermissionNotFoundError
from rfidsecuritysvc.model.media_perm import MediaPerm as Model

m = Model(1, 'media_id', 'media_name', 'media_desc', 2, 'permission_name', 'permission_id')


@patch('rfidsecuritysvc.api.media_perms.model')
def test_get(model):
    model.get.return_value = m
    assert api.get(m.id) == m.to_json()
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.media_perms.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get(m.id) == (f'Object with id "{m.id}" does not exist.', 404)
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.media_perms.model')
def test_search(model):
    m2 = Model(3, 'media_id2', 'media_name2', 'media_desc2', 4, 'permission_name2', 'permission_desc2')
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.media_perms.model')
def test_search_with_media_id(model):
    m2 = Model(3, 'media_id2', 'media_name2', 'media_desc2', 4, 'permission_name2', 'permission_desc2')
    model.list.return_value = [m, m2]
    assert api.search('test') == [m.to_json(), m2.to_json()]
    model.list.assert_called_once_with('test')


@patch('rfidsecuritysvc.api.media_perms.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.media_perms.model')
def test_post(model):
    model.create.return_value = None
    assert api.post(m.to_json()) == (None, 201)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.media_perms.model')
def test_post_Duplicate(model):
    model.create.side_effect = DuplicateError
    assert api.post(m.to_json()) == (f'Object with media_id "{m.media_id}" and permission_id "{m.permission_id}" already exists.', 409)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.media_perms.model')
def test_post_MediaNotFound(model):
    model.create.side_effect = MediaNotFoundError
    assert api.post(m.to_json()) == (f'No media found with id "{m.media_id}".', 400)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.media_perms.model')
def test_post_PermissionNotFound(model):
    model.create.side_effect = PermissionNotFoundError
    assert api.post(m.to_json()) == (f'No permission found with id "{m.permission_id}".', 400)
    model.create.assert_called_once_with(**m.to_json())


@patch('rfidsecuritysvc.api.media_perms.model')
def test_delete(model):
    model.delete.return_value = 1
    assert api.delete(m.id) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.media_perms.model')
def test_put(model):
    model.update.return_value = 1
    assert api.put(m.id, m.to_json_rw()) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **m.to_json_rw())


@patch('rfidsecuritysvc.api.media_perms.model')
def test_put_not_found(model):
    model.update.side_effect = MediaPermNotFoundError
    assert api.put(m.id, m.to_json_rw()) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **m.to_json_rw())
    model.create.assert_called_once_with(**m.to_json_rw())
