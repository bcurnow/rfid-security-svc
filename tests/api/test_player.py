from unittest.mock import patch

from rfidsecuritysvc.api import player as api
from rfidsecuritysvc.model.sound import Sound as Model


@patch('rfidsecuritysvc.api.player.model')
def test_get(model, wav_content):
    m = Model(1, 'test.wav', wav_content)
    model.get.return_value = m
    assert api.get(m.name) == m.content
    model.get.assert_called_once_with(m.name)


@patch('rfidsecuritysvc.api.player.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get('notfound') == ('Object with name "notfound" does not exist.', 404)
    model.get.assert_called_once_with('notfound')
