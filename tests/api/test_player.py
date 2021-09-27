from unittest.mock import patch

from rfidsecuritysvc.api import player as api


@patch('rfidsecuritysvc.api.player.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get('notfound') == ('Object with name "notfound" does not exist.', 404)
    model.get.assert_called_once_with('notfound')
