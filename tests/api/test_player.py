""" This only contains the not_found test as the others require the app context and are found in api-client """
from unittest.mock import patch

from rfidsecuritysvc.api import player as api


@patch('rfidsecuritysvc.api.player.model')
def test_get_not_found(model):
    model.get_by_name.return_value = None
    assert api.get('notfound') == ('Object with name "notfound" does not exist.', 404)
    model.get_by_name.assert_called_once_with('notfound')
