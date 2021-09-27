from datetime import datetime
from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import sounds as api
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
def test_delete(model):
    m = _model()
    model.delete.return_value = 1
    assert api.delete(m.name) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.name)


class ContentLength:
    def __init__(self, content_length):
        self.content_length = content_length


def test__content_length_use_content_length():
    assert api._content_length(ContentLength(5), []) == 5


def test__content_length_use_file_length():
    assert api._content_length(ContentLength(0), [1, 2, 3]) == 3


def _model(wav_content=b'', index=1):
    return Model(1, f'test{index}.wav', datetime.now().isoformat(timespec='seconds'), wav_content)


def _update(m):
    d = m.to_json().copy()
    del d['id']
    del d['last_update_timestamp']
    return d
