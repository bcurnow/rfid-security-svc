from unittest.mock import patch

from rfidsecuritysvc.api import authorized as api


@patch('rfidsecuritysvc.api.authorized.authorized')
def test_get_authorized(model, media_perms):
    model.authorized.return_value = media_perms[0]
    assert api.get('test', 1) == (media_perms[0].to_json(), 200)
    model.authorized.assert_called_once_with('test', 1)


@patch('rfidsecuritysvc.api.authorized.authorized')
def test_get_not_authorized(model):
    model.authorized.return_value = None
    assert api.get('test', 1) == (None, 403)
    model.authorized.assert_called_once_with('test', 1)
