import logging
import requests

from rfidsecuritysvc.model import config

""" The configuration key that specifies the RFID service URL."""
RFID_SERVICE_URL_CONFIG_KEY = 'RFID_SERVICE_URL'

def read(timeout):
    logger = logging.getLogger(__name__)
    url = config.get(RFID_SERVICE_URL_CONFIG_KEY)

    if url is None:
        return f"Unable to retrieve configuration key '{RFID_SERVICE_URL_CONFIG_KEY}', is the application configured correcctly?", 404
    
    logger.debug(f'Connecting to "{url}".')

    r = requests.get(url.value, params={'timeout': timeout}, timeout=timeout * 2)
    if r.status_code != 200:
        return None
    return r.text