from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import sounds as api
from rfidsecuritysvc.exception import DuplicateSoundError as DuplicateError
from rfidsecuritysvc.exception import SoundNotFoundError as NotFoundError
from rfidsecuritysvc.model.sound import Sound as Model


@patch('rfidsecuritysvc.api.sounds.model')
def test_get(model):
    m = _model(b'wav')
    model.get.return_value = m
    assert api.get(m.name) == m.to_json_with_content()
    model.get.assert_called_once_with(m.name)


@patch('rfidsecuritysvc.api.sounds.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get('notfound') == ('Object with name "notfound" does not exist.', 404)
    model.get.assert_called_once_with('notfound')


@patch('rfidsecuritysvc.api.sounds.model')
def test_search(model):
    m = _model()
    m2 = _model(index=2)
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.sounds.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.sounds.model')
def test_post(model, request, app, to_content):
    m = _model(b'wav')
    model.create.return_value = None
    with app.test_request_context(data=to_content(m)):
        assert api.post() == (None, 201)
    model.create.assert_called_once_with(m.name, m.content)


@patch('rfidsecuritysvc.api.sounds.model')
def test_post_no_content(model, app, to_content):
    m = _model()
    with app.test_request_context(data=to_content(m)):
        assert api.post() == ('audio/wav data is required', 400)
    model.create.assert_not_called()


@patch('rfidsecuritysvc.api.sounds.model')
def test_post_wrong_content_type(model, request, app, to_content):
    m = _model(b'wav')
    model.create.return_value = None
    with app.test_request_context(data=to_content(m, 'application/wrong')):
        assert api.post() == ('audio/wav data is required', 415)
    model.create.assert_not_called()


@patch('rfidsecuritysvc.api.sounds.model')
def test_post_Duplicate(model, app, to_content):
    m = _model(b'wav')
    model.create.side_effect = DuplicateError
    with app.test_request_context(data=to_content(m)):
        assert api.post() == (f'Object with name "{m.name}" already exists.', 409)
    model.create.assert_called_once_with(m.name, m.content)


@patch('rfidsecuritysvc.api.sounds.model')
def test_delete(model):
    m = _model()
    model.delete.return_value = 1
    assert api.delete(m.name) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.name)


@patch('rfidsecuritysvc.api.sounds.model')
def test_put(model, app, to_content):
    m = _model(b'wav')
    model.update.return_value = 1
    with app.test_request_context(data=to_content(m)):
        assert api.put(m.id) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, m.name, m.content)


@patch('rfidsecuritysvc.api.sounds.model')
def test_put_no_content(model, app, to_content):
    m = _model()
    model.update.return_value = 1
    with app.test_request_context(data=to_content(m)):
        assert api.put(m.id) == ('audio/wav data is required', 400)
    model.update.assert_not_called()


@patch('rfidsecuritysvc.api.sounds.model')
def test_put_wrong_content_type(model, app, to_content):
    m = _model(b'wav')
    model.update.return_value = 1
    with app.test_request_context(data=to_content(m, 'application/wrong')):
        assert api.put(m.id) == ('audio/wav data is required', 415)
    model.update.assert_not_called()


@patch('rfidsecuritysvc.api.sounds.model')
def test_put_already_exists(model, app, to_content):
    m = _model(b'wav')
    model.update.side_effect = NotFoundError
    with app.test_request_context(data=to_content(m)):
        assert api.put(m.id) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, m.name, m.content)
    model.create.assert_called_once_with(m.name, m.content)


class ContentLength:
    def __init__(self, content_length):
        self.content_length = content_length


def test__content_length_use_content_length():
    assert api._content_length(ContentLength(5), []) == 5


def test__content_length_use_file_length():
    assert api._content_length(ContentLength(0), [1, 2, 3]) == 3


def _model(wav_content=b'', index=1):
    return Model(1, f'test{index}.wav', wav_content)


def _update(m):
    d = m.to_json().copy()
    d.pop('name')
    return d
