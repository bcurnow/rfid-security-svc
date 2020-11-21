from unittest.mock import patch

api = 'reader'


@patch(f'rfidsecuritysvc.api.{api}.reader')
def test_search(reader, rh):
    reader.read.return_value = '80558aba5c3504'
    rh.assert_response(rh.open('get', f'{api}'), 200, reader.read.return_value)
    reader.read.assert_called_once_with(10)


@patch(f'rfidsecuritysvc.api.{api}.reader')
def test_search_noresults(reader, rh):
    reader.read.return_value = None
    rh.assert_response(rh.open('get', f'{api}'), 204, reader.read.return_value)
    reader.read.assert_called_once_with(10)
