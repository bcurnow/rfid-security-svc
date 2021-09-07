import requests

from flask import g, current_app

from rfidsecuritysvc.exception import ConfigNotFoundError
from rfidsecuritysvc.model import config

""" The configuration key that specifies the RFID service URL."""
RFID_SERVICE_URL_CONFIG_KEY = 'RFID_SERVICE_URL'


def read(timeout):
    current_app.logger.debug(f'Connecting to "{_rfid_service_url()}".')
    # make sure to set the timeout just in case, in theory, the web service will timeout
    # before the requests.get call does, but this ensures no hung threads
    r = requests.get(_rfid_service_url(), params={'timeout': timeout}, timeout=timeout * 2)
    print(r)
    print(r.status)
    print(r.text)
    if r.status != 200:
        return None
    return r.text


def _rfid_service_url():
    if 'rfid_service_url' not in g:
        # Get the URL from config
        url = config.get(RFID_SERVICE_URL_CONFIG_KEY)

        if not url:
            raise ConfigNotFoundError(f'Unable to retrieve configuration key "{RFID_SERVICE_URL_CONFIG_KEY}".')

        g.rfid_service_url = url.value

    return g.rfid_service_url
