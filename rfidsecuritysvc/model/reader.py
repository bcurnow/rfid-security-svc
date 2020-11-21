import os
import select

import evdev
from flask import g, current_app

from rfidsecuritysvc.exception import ConfigNotFoundError
from rfidsecuritysvc.model import config

""" The configuration key that specifies the RFID input device."""
RFID_DEVICE_CONFIG_KEY = 'RFID_DEVICE'

""" The timeout to use once we've determined there are events ready """
EVENT_READY_TIMEOUT = .01

""" Maps the hex key codes (0-9A-F) to characters so we can translate events from the reader."""
KEY_MAP = {
    'KEY_0': '0',
    'KEY_1': '1',
    'KEY_2': '2',
    'KEY_3': '3',
    'KEY_4': '4',
    'KEY_5': '5',
    'KEY_6': '6',
    'KEY_7': '7',
    'KEY_8': '8',
    'KEY_9': '9',
    'KEY_A': 'A',
    'KEY_B': 'B',
    'KEY_C': 'C',
    'KEY_D': 'D',
    'KEY_E': 'E',
    'KEY_F': 'F',
}


def read(timeout):
    current_app.logger.debug(f'Connecting to "{_device_name()}".')
    device = evdev.InputDevice(_device_name())

    try:
        # Use the supplied timeout to wait for a tag to be read, this timeout is longer than EVENT_READY_TIMEOUT
        # because we're waiting on a user to take an action
        if _event_ready(device, timeout):
            return _read_rfid(device)
    finally:
        # Need to catch RuntimeError due to https://github.com/gvalkov/python-evdev/issues/120
        try:
            device.close()
        except RuntimeError:
            pass


def _read_rfid(device):
    keep_reading = True
    data = []

    while keep_reading:
        _read_all_available_events(device, data)

        keep_reading = _event_ready(device, EVENT_READY_TIMEOUT)

    # All possible events have been read, convert the data to a string
    if data:
        return ''.join(data)


def _read_all_available_events(device, data):
    """ Reads all current ready events from device and adds the translated data to the data list."""
    try:
        for raw_event in device.read():
            event = evdev.categorize(raw_event)
            translated_event = _translate_event(event)
            if translated_event:
                data.append(translated_event)
    except BlockingIOError:
        # This indicates there are no more events to read
        pass


def _translate_event(event):
    """ Handle KeyEvents and specifically key_down events as these indicate data we care about. """
    if isinstance(event, evdev.events.KeyEvent) and event.keystate == evdev.events.KeyEvent.key_down:
        return KEY_MAP[event.keycode]


def _event_ready(device, timeout):
    """
    Uses select to block until a event is ready to be read from the device or until the timeout expires,
    returns True if there is at least one event, False otherwise."""
    # Open a non-blocking readonly file descriptor to the device
    fd = os.open(device, os.O_RDONLY | os.O_NONBLOCK)
    try:
        # Wait for an event
        r, w, x = select.select([fd], [], [], timeout)
    finally:
        os.close(fd)

    if not r:
        return False

    return True


def _device_name():
    if 'rfid_device_name' not in g:
        # Get the input device from config
        device_name = config.get(RFID_DEVICE_CONFIG_KEY)

        if not device_name:
            raise ConfigNotFoundError(f'Unable to retrieve configuration key "{RFID_DEVICE_CONFIG_KEY}".')

        g.rfid_device_name = device_name.value

    return g.rfid_device_name
