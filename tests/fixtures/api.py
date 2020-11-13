import json
import pytest

from werkzeug.datastructures import Headers
from werkzeug.test import EnvironBuilder

from rfidsecuritysvc.model import BaseModel


class ResponseHandler:
    def __init__(self, client, api_base, app, assert_model):
        self._client = client
        self._api_base = api_base
        self._app = app
        self._assert_model = assert_model


    def open(self, method, api, data=None, content_type='application/json'):
        h = Headers()
        # Add the default testing authorization header so the calls succeed
        h.add_header('X-RFIDSECURITYSVC-API-KEY', 'testing')

        if data is not None and 'application/json' in content_type:
            if isinstance(data, BaseModel):
                data = json.dumps(data.to_json())
            else:
                data = json.dumps(data)

        builder = EnvironBuilder(
            path=self._api_base + api,
            method=method.upper(),
            content_type='application/json',
            headers=h,
            charset='utf-8',
            data=data,
        )
        return self._client.open(builder)


    def assert_response(self, response, status_code=200, expected=None, headers=None):
        # Add some helpful debug info if we aren't going to be successful
        if response.status_code != status_code:
            print(f'{response.status} "{response.content_type}":\n{response.get_data(as_text=True)}\nHeaders:\n{response.headers}')

        assert response.status_code == status_code

        if expected is not None:
            assert response.data is not None

            actual = json.loads(response.get_data(as_text=True))

            if isinstance(expected, list):
                # assert the lengths of the lists to account for zero-length lists
                assert len(expected) == len(actual)

                for index, item in enumerate(expected):
                    if isinstance(item, BaseModel):
                        self._assert_model(item.to_json(), actual[index])
                    else:
                        assert item == actual[index]
            else:
                if isinstance(expected, BaseModel):
                    self._assert_model(expected.to_json(), actual)
                else:
                    assert expected == actual

        if headers is not None:
            for header, value in headers.items():
                assert response.headers.get(header) == value


@pytest.fixture
def rh(client, api_base, app, assert_model):
    return ResponseHandler(client, api_base, app, assert_model)


@pytest.fixture
def test_api_key():
    # This value is 'testing'
    return 'pbkdf2:sha256:150000$gQ68PeFG$8171ee457bac33eff68dce8d2d1dc84c32d9b39ef21c0623ebfa384a210cb44d'


@pytest.fixture
def api_base():
    return '/api/v1.0/'


