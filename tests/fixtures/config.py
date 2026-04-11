import pytest

@pytest.fixture(scope='session')
def configs(test_api_key):
    from rfidsecuritysvc.model.config import Config

    # The DB will return these ordered by key, please build the list accordingly
    return [Config('ADMIN_API_KEY', test_api_key)]


@pytest.fixture(scope='session')
def creatable_config():
    from rfidsecuritysvc.model.config import Config

    return Config('creatable key', 'creatable value')


@pytest.fixture(autouse=True, scope='session')
def add_config_helpers(monkeypatch_session):
    from rfidsecuritysvc.model.config import Config

    def convert(self):
        return self.to_json()

    monkeypatch_session.setattr(Config, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Config, 'test_update', convert, raising=False)
