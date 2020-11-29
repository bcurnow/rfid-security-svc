import os
import select

from flask import g, current_app

from rfidreader import RFIDReader
from rfidsecuritysvc.exception import ConfigNotFoundError
from rfidsecuritysvc.model import config

""" The configuration key that specifies the RFID input device."""
RFID_DEVICE_CONFIG_KEY = 'RFID_DEVICE'


def read(timeout):
    current_app.logger.debug(f'Connecting to "{_device_name()}".')
    reader = RFIDReader(_device_name())
    # Need to grab the device before reading, we're assuming we're running both the API and the main reader loop
    # on the same host and therefore, the main reader loop would normally read the tag before we could.
    # Grabbing the device makes it exclusive to our process and allows us to read the next tag scanned.
    print(reader.device)
    reader.device.grab()
    try:
        return reader.read(timeout)
    finally:
        reader.device.ungrab()


def _device_name():
    if 'rfid_device_name' not in g:
        # Get the input device from config
        device_name = config.get(RFID_DEVICE_CONFIG_KEY)

        if not device_name:
            raise ConfigNotFoundError(f'Unable to retrieve configuration key "{RFID_DEVICE_CONFIG_KEY}".')

        g.rfid_device_name = device_name.value

    return g.rfid_device_name
