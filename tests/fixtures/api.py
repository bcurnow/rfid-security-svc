import json
import pytest

from rfidsecuritysvc.model import BaseModel


class ResponseHandler:
    def __init__(self, client, api_base, app, assert_model):
        self._client = client
        self._api_base = api_base
        self._app = app
        self._assert_model = assert_model

    def open(self, method, api, data=None, content_type='application/json', headers={}):
        # Add the default testing authorization header so the calls succeed
        request_headers = {'X-RFIDSECURITYSVC-API-KEY': 'testing'}
        request_headers.update(headers)

        request_content = None
        request_data = None
        request_files = None
        if data is not None:
            if 'application/json' in content_type:
                request_headers['Content-Type'] = 'application/json'
                # We have data and it is supposed to be JSON, we need to conver the object to JSON
                if isinstance(data, BaseModel):
                    # BaseModel has two methods monkeypatched in:
                    # - test_update - Removes the attributes that are readOnly
                    # - test_create - Performs any conversion necessary to call create
                    if method == 'put':
                        request_content = json.dumps(data.test_update())
                    elif method == 'post':
                        request_content = json.dumps(data.test_create())
                    else:
                        request_content = json.dumps(data.to_json())
                else:
                    request_content = json.dumps(data)
            elif 'multipart/form-data' in content_type:
                # We don't update the headers here because request will set it correctly because we're providing data and files
                # This must be submitted as a tuple containing the form data (any text fields) and the files.
                request_data, request_files = data
            else:
                request_headers['Content-Type'] = content_type
                # We have data but it's not supposed a content type we explicitly handle, we'll populate data and assume that everything goes to plan
                request_data = data

        return self._client.request(method=method.upper(), url=self._api_base + api, content=request_content, data=request_data, files=request_files, headers=request_headers)

    def assert_response(self, response, status_code=200, expected=None, headers=None):
        # Add some helpful debug info if we aren't going to be successful
        if response.status_code != status_code:
            content_type = response.headers.get('content-type', '')
            print(f'{response.status_code} "{content_type}":\n{response.text}\nHeaders:\n{dict(response.headers)}')

        assert response.status_code == status_code

        if expected is not None:
            assert response.content is not None

            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                actual = response.json()
            else:
                actual = response.content

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
        # testing but doesn't want to keep the single line assert semantics
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
