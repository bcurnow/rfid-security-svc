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

    def open(self, method, api, data=None, content_type='application/json', headers={}):
        h = Headers()
        # Add the default testing authorization header so the calls succeed
        h.add_header('X-RFIDSECURITYSVC-API-KEY', 'testing')
        for header, value in headers.items():
            h.add_header(header, value)

        if data is not None and 'application/json' in content_type:
            if isinstance(data, BaseModel):
                # BaseModel has to methods monkeypatched in:
                # - test_update - Removes the attributes that are readOnly
                # - test_create - Performs any conversion necessary to call create
                if method == 'put':
                    data = json.dumps(data.test_update())
                elif method == 'post':
                    data = json.dumps(data.test_create())
                else:
                    print("in the else:", type(data), data)
                    data = json.dumps(data.to_json())
            else:
                data = json.dumps(data)

        builder = EnvironBuilder(
            path=self._api_base + api,
            method=method.upper(),
            content_type=content_type,
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

            if 'application/json' in response.content_type:
                actual = json.loads(response.get_data(as_text=True))
            else:
                actual = response.get_data()

            if isinstance(expected, list):
                # assert the lengths of the lists to account for zero-length lists
                assert len(expected) == len(actual)

                for index, item in enumerate(expected):
                    if isinstance(item, BaseModel):
                        self._assert_model(item, actual[index])
                    else:
                        assert item == actual[index]
            else:
                if isinstance(expected, BaseModel):
                    self._assert_model(expected, actual)
                else:
                    assert expected == actual

        if headers is not None:
            for header, value in headers.items():
                assert response.headers.get(header) == value
        # Return the response that was passed into us, this is helpful if the test wants to do some additional
        # testing but doesn't wants to keep the single line assert semantics
        return response


@pytest.fixture(scope='session')
def rh(client, api_base, app, assert_model):
    return ResponseHandler(client, api_base, app, assert_model)


@pytest.fixture(scope='session')
def test_api_key():
    # This value is 'testing'
    return 'pbkdf2:sha256:150000$gQ68PeFG$8171ee457bac33eff68dce8d2d1dc84c32d9b39ef21c0623ebfa384a210cb44d'


@pytest.fixture(scope='session')
def api_base():
    return '/api/v1.0/'


@pytest.fixture(scope='session')
def monkeypatch_session():
    from _pytest.monkeypatch import MonkeyPatch
    m = MonkeyPatch()
    yield m
    m.undo()
