from unittest.mock import patch

from rfidsecuritysvc.api import reader as api


@patch('rfidsecuritysvc.api.reader.reader')
def test_search(reader):
    reader.read.return_value = '80558ABA5C3504'
    assert api.search() == reader.read.return_value
    reader.read.assert_called_once_with(10)


@patch('rfidsecuritysvc.api.reader.reader')
def test_search_noresult(reader):
    reader.read.return_value = None
    assert api.search() == reader.read.return_value
    reader.read.assert_called_once_with(10)


@patch('rfidsecuritysvc.api.reader.reader')
def test_search_timeout(reader):
    reader.read.return_value = '80558ABA5C3504'
    assert api.search(25) == reader.read.return_value
    reader.read.assert_called_once_with(25)
