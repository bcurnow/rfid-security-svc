from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'config'


def test_get(rh, configs):
    rh.assert_response(rh.open('get', f'{api}/{configs[0].key}'), 200, configs[0])


def test_get_notfound(rh, configs):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, configs):
    rh.assert_response(rh.open('get', f'{api}'), 200, configs)


@patch(f'rfidsecuritysvc.api.{api}.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_config):
    rh.assert_response(rh.open('post', f'{api}', creatable_config), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_config.key}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_config.key}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_config.key}'), 404)


def test_post_duplicate(rh, configs):
    rh.assert_response(rh.open('post', f'{api}', configs[0]), 409)


def test_delete(rh, creatable_config):
    rh.assert_response(rh.open('post', f'{api}', creatable_config), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_config.key}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_config.key}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_config.key}'), 404)


def test_delete_notfound(rh, creatable_config):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_config.key}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, configs):
    rh.assert_response(rh.open('put', f'{api}/{configs[0].key}', configs[0]), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_notfound(rh, creatable_config):
    rh.assert_response(rh.open('put', f'{api}/{creatable_config.key}', creatable_config), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_config.key}', creatable_config), 200, headers={RECORD_COUNT_HEADER: '1'})
