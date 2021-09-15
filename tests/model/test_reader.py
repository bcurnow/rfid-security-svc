import pytest
from unittest.mock import patch, PropertyMock

from flask import g

import rfidsecuritysvc.model.reader as model
from rfidsecuritysvc.exception import ConfigNotFoundError
from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.reader import RFID_SERVICE_URL_CONFIG_KEY

timeout = 10


@patch('rfidsecuritysvc.model.reader.requests')
@patch('rfidsecuritysvc.model.reader.config')
def test_read(config, requests, app):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    request_mock = requests.get.return_value
    status = PropertyMock(return_value=200)
    text = PropertyMock(return_value='08')
    type(request_mock).status_code = status
    type(request_mock).text = text

    with app.app_context():
        assert model.read(timeout) == '08'

    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    requests.get.assert_called_once_with('http://localhost:8080/get_uid', params={'timeout':timeout}, timeout=timeout *2)


@patch('rfidsecuritysvc.model.reader.requests')
@patch('rfidsecuritysvc.model.reader.config')
def test_read_204(config, requests, app):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    request_mock = requests.get.return_value
    status = PropertyMock(return_value=204)
    type(request_mock).status_code = status

    with app.app_context():
        assert model.read(timeout) is None

    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    requests.get.assert_called_once_with('http://localhost:8080/get_uid', params={'timeout':timeout}, timeout=timeout *2)


@patch('rfidsecuritysvc.model.reader.config')
def test__rfid_service_url_name(config, app):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    with app.app_context():
        assert 'rfid_service_url' not in g
        assert model._rfid_service_url() == config.get.return_value.value
        assert 'rfid_service_url' in g
        assert g.rfid_service_url == config.get.return_value.value
        # Assert the call again to make sure we're returning the cached value
        assert model._rfid_service_url() == config.get.return_value.value
    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)


@patch('rfidsecuritysvc.model.reader.config')
def test__rfid_service_url_noconfig(config, app):
    config.get.return_value = None
    with app.app_context():
        with pytest.raises(ConfigNotFoundError):
            model._rfid_service_url()
    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
