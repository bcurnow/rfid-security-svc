from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'guests'


def test_get(rh, guests):
    rh.assert_response(rh.open('get', f'{api}/{guests[0].id}'), 200, guests[0])


def test_get_notfound(rh):
    rh.assert_response(rh.open('get', f'{api}/-1'), 404)


def test_search(rh, guests):
    rh.assert_response(rh.open('get', f'{api}'), 200, guests)


@patch(f'rfidsecuritysvc.api.{api}.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_guest):
    rh.assert_response(rh.open('post', f'{api}', creatable_guest), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_guest.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_guest.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_guest.id}'), 404)


def test_post_duplicate(rh, guests):
    rh.assert_response(rh.open('post', f'{api}', guests[0]), 409)


def test_delete(rh, creatable_guest):
    rh.assert_response(rh.open('post', f'{api}', creatable_guest), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_guest.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_guest.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_guest.id}'), 404)


def test_delete_notfound(rh, creatable_guest):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_guest.id}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, guests):
    rh.assert_response(rh.open('put', f'{api}/{guests[0].id}', guests[0]), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_notfound(rh, creatable_guest):
    rh.assert_response(rh.open('put', f'{api}/{creatable_guest.id}', creatable_guest), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_guest.id}', creatable_guest), 200, headers={RECORD_COUNT_HEADER: '1'})
