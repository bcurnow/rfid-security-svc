from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'permission'


def test_get(rh, permissions):
    rh.assert_response(rh.open('get', f'{api}/{permissions[0].name}'), 200, permissions[0])


def test_get_notfound(rh, permissions):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, permissions):
    rh.assert_response(rh.open('get', f'{api}'), 200, permissions)


@patch(f'rfidsecuritysvc.api.{api}.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_permission):
    rh.assert_response(rh.open('post', f'{api}', creatable_permission), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_permission.name}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_permission.name}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_permission.name}'), 404)


def test_post_duplicate(rh, permissions):
    rh.assert_response(rh.open('post', f'{api}', permissions[0]), 409)


def test_delete(rh, creatable_permission):
    rh.assert_response(rh.open('post', f'{api}', creatable_permission), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_permission.name}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_permission.name}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_permission.name}'), 404)


def test_delete_notfound(rh, creatable_permission):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_permission.name}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, permissions):
    rh.assert_response(rh.open('put', f'{api}/{permissions[0].name}', permissions[0]), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_notfound(rh, creatable_permission):
    rh.assert_response(rh.open('put', f'{api}/{creatable_permission.name}', creatable_permission), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_permission.name}', creatable_permission), 200, headers={RECORD_COUNT_HEADER: '1'})
