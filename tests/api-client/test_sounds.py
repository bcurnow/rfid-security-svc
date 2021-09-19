from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'sounds'


def test_get(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/{sounds[0].name}'), 200, sounds[0].to_json_with_content())


def test_get_notfound(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}'), 200, sounds)


@patch(f'rfidsecuritysvc.api.{api}.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_sound, to_content):
    rh.assert_response(rh.open('post', f'{api}', to_content(creatable_sound), 'multipart/form-data'), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.name}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.name}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.name}'), 404)


def test_post_duplicate(rh, sounds, to_content):
    rh.assert_response(rh.open('post', f'{api}', to_content(sounds[0]), 'multipart/form-data'), 409)


def test_delete(rh, creatable_sound, to_content):
    rh.assert_response(rh.open('post', f'{api}', to_content(creatable_sound), 'multipart/form-data'), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.name}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.name}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.name}'), 404)


def test_delete_notfound(rh, creatable_sound):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.name}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, sounds, to_content):
    rh.assert_response(rh.open('put', f'{api}/{sounds[0].id}', to_content(sounds[0]), 'multipart/form-data'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_notfound(rh, creatable_sound, to_content):
    rh.assert_response(rh.open('put',
                               f'{api}/{creatable_sound.id}',
                               to_content(creatable_sound),
                               'multipart/form-data'
                               ), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.name}', creatable_sound), 200, headers={RECORD_COUNT_HEADER: '1'})
