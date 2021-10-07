from unittest.mock import patch

import rfidsecuritysvc.model.authorized as model
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.authorized import MediaConfig
from rfidsecuritysvc.exception import PermissionNotFoundError, MediaPermNotFoundError


@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized(media_perm, media_perms):
    media_perm.get_by_media_and_perm.return_value = media_perms[0]
    expected = MediaConfig(media_perms[0],
                Guest(-1, 'not yet implemented', 'not yet implemented'),
                -1,
                'not yet implemented',
                0x000000)
    assert model.authorized('test', 'test_perm') == expected
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 'test_perm')


@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized_invalid_perm_name(media_perm):
    media_perm.get_by_media_and_perm.side_effect = PermissionNotFoundError
    assert model.authorized('test', 'test_perm') is None
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 'test_perm')


@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized_invalid_media_id(media_perm):
    media_perm.get_by_media_and_perm.side_effect = MediaPermNotFoundError
    assert model.authorized('test', 'test_perm') is None
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 'test_perm')
