import pytest
import time
from unittest.mock import call, patch

from flask import g

import rfidsecuritysvc.model.reader as model
from rfidsecuritysvc.exception import ConfigNotFoundError
from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.reader import RFID_DEVICE_CONFIG_KEY

timeout = 10


@patch('rfidsecuritysvc.model.reader.RFIDReader')
@patch('rfidsecuritysvc.model.reader.config')
def test_read(config, RFIDReader, app):
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    reader = RFIDReader.return_value
    reader.read.return_value = '08'
    device = reader.device

    with app.app_context():
        assert model.read(timeout) == '08'

    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    RFIDReader.assert_called_once_with('/dev/test')
    device.grab.assert_called_once()
    reader.read.assert_called_once_with(timeout)
    device.ungrab.assert_called_once()


@patch('rfidsecuritysvc.model.reader.config')
def test__device_name(config, app):
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    with app.app_context():
        assert 'rfid_device_name' not in g
        assert model._device_name() == config.get.return_value.value
        assert 'rfid_device_name' in g
        assert g.rfid_device_name == config.get.return_value.value
        # Assert the call again to make sure we're returning the cached value
        assert model._device_name() == config.get.return_value.value
    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)


@patch('rfidsecuritysvc.model.reader.config')
def test__device_name_noconfig(config, app):
    config.get.return_value = None
    with app.app_context():
        with pytest.raises(ConfigNotFoundError):
            model._device_name()
    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
