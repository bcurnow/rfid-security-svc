import pytest
from unittest.mock import patch

from rfidsecuritysvc.api import authorized as api

@patch('rfidsecuritysvc.api.authorized.authorized')
def test_get_authorized(model):
    model.authorized.return_value = True
    assert api.get('test', 1) == (None, 200)
    model.authorized.assert_called_once_with('test', 1)

@patch('rfidsecuritysvc.api.authorized.authorized')
def test_get_not_authorized(model):
    model.authorized.return_value = False
    assert api.get('test', 1) == (None, 403)
    model.authorized.assert_called_once_with('test', 1)
