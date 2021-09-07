from unittest.mock import patch

from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.reader import RFID_SERVICE_URL_CONFIG_KEY


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_url(config, list, runner):
    config.get.return_value = None
    config.create.return_value = None
    list.return_value = []
    runner.invoke(args=['reader', 'set-url', 'http://localhost:8080/get_uid'], color=True)
    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    config.create.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    list.assert_called_once()


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_url_alreadyexists(config, list, runner, assert_output):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://otherurl/get_uid')
    config.update.return_value = 1
    list.return_value = [Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')]
    result = runner.invoke(args=['reader', 'set-url', 'http://localhost:8080/get_uid'], input='y', color=True)
    assert_output(result,
                  f'There is already a key "{RFID_SERVICE_URL_CONFIG_KEY}" '
                  'with value "http://otherurl/get_uid", do you want to replace with "http://localhost:8080/get_uid"?',
                  0)
    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    config.update.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    list.assert_called_once()


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_url_alreadyexists_yes_flag(config, list, runner, assert_output):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://otherurl/get_uid')
    config.update.return_value = 1
    list.return_value = [Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')]
    result = runner.invoke(args=['reader', 'set-url', 'http://localhost:8080/get_uid', '--yes'], color=True)
    assert f'There is already a key "{RFID_SERVICE_URL_CONFIG_KEY}" ' \
           'with value "http://otherurl/get_uid", do you want to replace with "http://localhost:8080/get_uid"?' not in result.output
    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    config.update.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY, 'http://localhost:8080/get_uid')
    list.assert_called_once()


@patch('rfidsecuritysvc.cli.reader.list')
@patch('rfidsecuritysvc.cli.reader.config')
def test_set_url_alreadyexists_n(config, list, runner, assert_output):
    config.get.return_value = Config(RFID_SERVICE_URL_CONFIG_KEY, 'http://otherurl/get_uid')
    result = runner.invoke(args=['reader', 'set-url', 'http://localhost:8080/get_uid'], input='n', color=True)
    assert_output(result,
                  f'There is already a key "{RFID_SERVICE_URL_CONFIG_KEY}" '
                  'with value "http://otherurl/get_uid", do you want to replace with "http://localhost:8080/get_uid"?',
                  1)
    config.get.assert_called_once_with(RFID_SERVICE_URL_CONFIG_KEY)
    config.create.assert_not_called()
    config.update.assert_not_called()
    list.assert_not_called()
