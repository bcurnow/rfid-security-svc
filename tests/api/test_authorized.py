from unittest.mock import patch

from rfidsecuritysvc.api import authorized as api
from rfidsecuritysvc.model.authorized import MediaConfig


@patch('rfidsecuritysvc.api.authorized.authorized')
def test_get(model, media_perms):
    mc = MediaConfig(media_perms[0], None, None, None, None)
    model.authorized.return_value = mc
    assert api.get('test', 1) == mc.to_json()
    model.authorized.assert_called_once_with('test', 1)


@patch('rfidsecuritysvc.api.authorized.authorized')
def test_get_not_found(model, media_perms):
    model.authorized.return_value = None
    assert api.get('test', 1) == (None, 403)
    model.authorized.assert_called_once_with('test', 1)
