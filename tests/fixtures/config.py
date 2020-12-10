import pytest

from rfidsecuritysvc.model.config import Config


@pytest.fixture(scope='session')
def configs(test_api_key):
    # The DB will return these ordered by key, please build the list accordingly
    return [Config('ADMIN_API_KEY', test_api_key)]


@pytest.fixture(scope='session')
def creatable_config():
    return Config('creatable key', 'creatable value')
