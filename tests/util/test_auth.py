import pytest

from unittest.mock import patch

from connexion.exceptions import OAuthProblem

from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.util import auth
from rfidsecuritysvc.util.auth import API_KEY_CONFIG_KEY, API_KEY_SIZE

@patch('rfidsecuritysvc.util.auth.config')
@patch('rfidsecuritysvc.util.auth.generate_password_hash')
@patch('rfidsecuritysvc.util.auth.token_urlsafe')
def test_generate_api_key(token_urlsafe, generate_password_hash, config):
    token_urlsafe.return_value = 'test'
    config.delete.return_value = 0
    config.create.return_value = None
    generate_password_hash.return_value = 'test'
    assert auth.generate_api_key() == 'test' 
    token_urlsafe.assert_called_once_with(API_KEY_SIZE)
    config.delete.assert_called_once_with(API_KEY_CONFIG_KEY)
    config.create.assert_called_once_with(API_KEY_CONFIG_KEY, 'test')

@patch('rfidsecuritysvc.util.auth.config')
@patch('rfidsecuritysvc.util.auth.check_password_hash')
def test_verify_apikey(check_password_hash, config):
    config.get.return_value = Config(API_KEY_CONFIG_KEY, 'test')
    check_password_hash.return_value = True
    assert auth.verify_apikey('test', None) == {'uid': 'Admin API Key'}
    config.get.assert_called_once_with(API_KEY_CONFIG_KEY)
    check_password_hash.assert_called_once_with('test', 'test')

@patch('rfidsecuritysvc.util.auth.config')
@patch('rfidsecuritysvc.util.auth.check_password_hash')
def test_verify_apikey_false(check_password_hash, config):
    config.get.return_value = Config(API_KEY_CONFIG_KEY, 'nottest')
    check_password_hash.return_value = False
    with pytest.raises(OAuthProblem) as einfo:
        auth.verify_apikey('test', None)

    assert einfo.value.description == 'Invalid authentication: "test"'
    config.get.assert_called_once_with(API_KEY_CONFIG_KEY)
    check_password_hash.assert_called_once_with('nottest', 'test')

