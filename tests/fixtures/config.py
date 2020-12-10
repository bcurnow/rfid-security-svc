import pytest


import rfidsecuritysvc
from rfidsecuritysvc.model.config import Config


@pytest.fixture(scope='session')
def configs(test_api_key):
    return [Config('ADMIN_API_KEY', test_api_key)]


@pytest.fixture(scope='session')
def creatable_config():
    return Config('creatable key', 'creatable value')
