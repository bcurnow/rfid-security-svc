import pytest
import time
from unittest.mock import call, patch

import evdev as evdev_module
from flask import g

import rfidsecuritysvc.model.reader as model
from rfidsecuritysvc.exception import ConfigNotFoundError
from rfidsecuritysvc.model.config import Config
from rfidsecuritysvc.model.reader import RFID_DEVICE_CONFIG_KEY, EVENT_READY_TIMEOUT

timeout = 10


@patch('rfidsecuritysvc.model.reader.config')
@patch('rfidsecuritysvc.model.reader.evdev')
@patch('rfidsecuritysvc.model.reader.select')
@patch('rfidsecuritysvc.model.reader.os')
def test_read(os, select, evdev, config, app):
    # Make sure to that KeyEvent is a type so the isinstance check works
    evdev.events.KeyEvent = evdev_module.events.KeyEvent
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    device = evdev.InputDevice.return_value
    os.open.return_value = 1
    select.select.side_effect = [([1], [], []), ([], [], [])]
    generator = device.read.return_value
    raw_events = [_raw_event(), _raw_event(code=9)]
    generator.__iter__.return_value = iter(raw_events)
    categorize = evdev.categorize
    categorize.side_effect = list(map(lambda event: _key_event(event), raw_events))

    with app.app_context():
        assert model.read(timeout) == '08'

    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    os.open.assert_has_calls(list(map(lambda device, perm: call(device, perm), [device] * 2, [os.O_RDONLY.__or__()] * 2)), any_order=True)
    select.select.assert_has_calls(
        list(map(lambda r, w, x, timeout: call(r, w, x, timeout), [[1]] * 2, [[]] * 2, [[]] * 2, [timeout, EVENT_READY_TIMEOUT])), any_order=True)
    os.close.assert_has_calls([call(1), call(1)], any_order=True)
    device.read.assert_called_once()
    generator.__iter__.assert_called_once()
    categorize.assert_has_calls(list(map(lambda event: call(event), raw_events)), any_order=True)
    device.close.assert_called_once()


@patch('rfidsecuritysvc.model.reader.config')
@patch('rfidsecuritysvc.model.reader.evdev')
@patch('rfidsecuritysvc.model.reader.select')
@patch('rfidsecuritysvc.model.reader.os')
def test_read_timeout(os, select, evdev, config, app):
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    device = evdev.InputDevice.return_value
    os.open.return_value = 1
    select.select.side_effect = [([], [], [])]

    with app.app_context():
        assert model.read(timeout) is None

    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    os.open.assert_called_once_with(device, os.O_RDONLY.__or__())
    select.select.assert_called_once_with([1], [], [], timeout)
    os.close.assert_called_once_with(1)
    device.close.assert_called_once()


@patch('rfidsecuritysvc.model.reader.config')
@patch('rfidsecuritysvc.model.reader.evdev')
@patch('rfidsecuritysvc.model.reader.select')
@patch('rfidsecuritysvc.model.reader.os')
def test_read_close_RuntimeError(os, select, evdev, config, app):
    config.get.return_value = Config(RFID_DEVICE_CONFIG_KEY, '/dev/test')
    device = evdev.InputDevice.return_value
    os.open.return_value = 1
    select.select.side_effect = [([], [], [])]
    device.close.side_effect = RuntimeError

    with app.app_context():
        assert model.read(timeout) is None

    config.get.assert_called_once_with(RFID_DEVICE_CONFIG_KEY)
    os.open.assert_called_once_with(device, os.O_RDONLY.__or__())
    select.select.assert_called_once_with([1], [], [], timeout)
    os.close.assert_called_once_with(1)
    device.close.assert_called_once()


@patch('rfidsecuritysvc.model.reader.evdev')
def test__read_all_available_events_BlockingIOError(evdev):
    device = evdev.InputDevice.return_value
    device.read.side_effect = BlockingIOError
    data = []
    model._read_all_available_events(device, data)
    assert data == []


@patch('rfidsecuritysvc.model.reader._translate_event')
@patch('rfidsecuritysvc.model.reader.evdev')
def test__read_all_available_events_translate_returns_none(evdev, translate_event):
    device = evdev.InputDevice.return_value
    generator = device.read.return_value
    raw_events = [_raw_event()]
    generator.__iter__.return_value = iter(raw_events)
    categorize = evdev.categorize
    key_event = _key_event(raw_events[0])
    categorize.return_value = key_event
    translate_event.return_value = None

    data = []
    model._read_all_available_events(device, data)
    assert data == []

    device.read.assert_called_once()
    generator.__iter__.assert_called_once()
    categorize.assert_called_once_with(raw_events[0])
    translate_event.assert_called_once_with(key_event)


def test__translate_event_wrong_event_type():
    assert not model._translate_event('this is not an event type')


def test__translate_event_wrong_keystate():
    assert not model._translate_event(_key_event(_raw_event(value=0)))


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


def _raw_event(value=1, code=11):
    class Event:
        def __init__(self, value, code):
            self.value = value
            self.code = code

        def timestamp(self):
            return time.time()

    return Event(value, code)


def _key_event(event):
    return evdev_module.events.KeyEvent(event)
