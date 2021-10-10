import pytest

from rfidsecuritysvc.model.config import Config


@pytest.fixture(scope='session')
def configs(test_api_key):
    # The DB will return these ordered by key, please build the list accordingly
    return [Config('ADMIN_API_KEY', test_api_key)]


@pytest.fixture(scope='session')
def creatable_config():
    return Config('creatable key', 'creatable value')


@pytest.fixture(autouse=True, scope='session')
def add_config_helpers(monkeypatch_session):
    def convert(self):
        return self.__dict__.copy()

    monkeypatch_session.setattr(Config, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Config, 'test_update', convert, raising=False)
