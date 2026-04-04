from unittest.mock import patch, PropertyMock

import rfidsecuritysvc.model.reader as model
from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.reader import RFID_SERVICE_URL_CONFIG_KEY

timeout = 10


@patch('rfidsecuritysvc.model.reader.requests')
@patch('rfidsecuritysvc.model.reader.config')
def test_read(config, requests):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    request_mock = requests.get.return_value
    status = PropertyMock(return_value=200)
    text = PropertyMock(return_value='08')
    type(request_mock).status_code = status
    type(request_mock).text = text

    assert model.read(timeout) == '08'

    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    requests.get.assert_called_once_with(
        'http://localhost:8080/get_uid',
        params={'timeout': timeout},
        timeout=timeout * 2,
    )


@patch('rfidsecuritysvc.model.reader.requests')
@patch('rfidsecuritysvc.model.reader.config')
def test_read_204(config, requests):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    request_mock = requests.get.return_value
    status = PropertyMock(return_value=204)
    type(request_mock).status_code = status

    assert model.read(timeout) is None

    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    requests.get.assert_called_once_with(
        'http://localhost:8080/get_uid',
        params={'timeout': timeout},
        timeout=timeout * 2,
    )