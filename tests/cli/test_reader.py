from unittest.mock import patch

from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.reader import RFID_DEVICE_CONFIG_KEY


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_device_name(config, list, runner):
    config.get.return_value = None
    config.create.return_value = None
    list.return_value = []
    result = runner.invoke(args=['reader', 'set-device-name', '/dev/test'], color=True)
    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    config.create.assert_called_once_with(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    list.assert_called_once()


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_device_name_alreadyexists(config, list, runner, assert_output):
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/othervalue')
    config.update.return_value = 1
    list.return_value = [Config(RFID_DEVICE_CONFIG_KEY, '/dev/test')]
    result = runner.invoke(args=['reader', 'set-device-name', '/dev/test'], input='y', color=True)
    assert_output(result, f'There is already a key "{RFID_DEVICE_CONFIG_KEY}" with value "/dev/othervalue", do you want to replace with "/dev/test"?', 0)
    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    config.update.assert_called_once_with(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    list.assert_called_once()


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_device_name_alreadyexists_n(config, list, runner, assert_output):
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/othervalue')
    result = runner.invoke(args=['reader', 'set-device-name', '/dev/test'], input='n', color=True)
    assert_output(result, f'There is already a key "{RFID_DEVICE_CONFIG_KEY}" with value "/dev/othervalue", do you want to replace with "/dev/test"?', 1)
    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    config.create.assert_not_called()
    config.update.assert_not_called()
    list.assert_not_called()
