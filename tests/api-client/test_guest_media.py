from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest_media import GuestMedia as Model

api = 'guest-media'


def test_get(rh, guest_medias):
    rh.assert_response(rh.open('get', f'{api}/{guest_medias[0].id}'), 200, guest_medias[0])


def test_get_notfound(rh, guest_medias):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, guest_medias):
    rh.assert_response(rh.open('get', f'{api}'), 200, guest_medias)


def test_search_with_guest_id(rh, guest_medias):
    rh.assert_response(rh.open('get', f'{api}?guest_id={guest_medias[1].guest.id}'), 200, [guest_medias[1]])


@patch('rfidsecuritysvc.api.guest_media.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_guest_media):
    p = creatable_guest_media
    rh.assert_response(rh.open('post', f'{api}', p), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 404)


def test_post_duplicate(rh, guest_medias):
    rh.assert_response(rh.open('post', f'{api}', guest_medias[0]), 409)


def test_post_guest_notfound(rh, creatable_guest_media, creatable_guest):
    m = Model(creatable_guest_media.id,
              creatable_guest,
              creatable_guest_media.media,
              creatable_guest_media.sound,
              creatable_guest_media.color)
    rh.assert_response(rh.open('post', f'{api}', m), 400)


def test_post_media_notfound(rh, creatable_guest_media, creatable_media):
    m = Model(creatable_guest_media.id,
              creatable_guest_media.guest,
              creatable_media,
              creatable_guest_media.sound,
              creatable_guest_media.color)
    rh.assert_response(rh.open('post', f'{api}', m), 400)


def test_post_sound_notfound(rh, creatable_guest_media, creatable_sound):
    m = Model(creatable_guest_media.id,
              creatable_guest_media.guest,
              creatable_guest_media.media,
              creatable_sound,
              creatable_guest_media.color)
    rh.assert_response(rh.open('post', f'{api}', m), 400)


def test_delete(rh, creatable_guest_media):
    p = creatable_guest_media
    rh.assert_response(rh.open('post', f'{api}', p.test_create()), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 404)


def test_delete_notfound(rh, creatable_guest_media):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_guest_media.id}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, creatable_guest_media):
    p = creatable_guest_media
    updated_p = Model(creatable_guest_media.id,
                      creatable_guest_media.guest,
                      creatable_guest_media.media,
                      creatable_guest_media.sound,
                      Color(0xFEDCBA))

    rh.assert_response(rh.open('post', f'{api}', p.test_create()), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('put', f'{api}/{p.id}', updated_p.test_update()), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200, updated_p)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_notfound(rh, creatable_guest_media):
    p = creatable_guest_media

    rh.assert_response(rh.open('put', f'{api}/{p.id}', p.test_update()), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200, p)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_guest_notfound(rh, creatable_guest_media, creatable_guest):
    p = creatable_guest_media
    updated_p = Model(creatable_guest_media.id,
                      creatable_guest,
                      creatable_guest_media.media,
                      creatable_guest_media.sound,
                      Color(0xFEDCBA))

    rh.assert_response(rh.open('post', f'{api}', p.test_create()), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('put', f'{api}/{p.id}', updated_p.test_update()), 400)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_media_notfound(rh, creatable_guest_media, creatable_media):
    p = creatable_guest_media
    updated_p = Model(creatable_guest_media.id,
                      creatable_guest_media.guest,
                      creatable_media,
                      creatable_guest_media.sound,
                      Color(0xFEDCBA))

    rh.assert_response(rh.open('post', f'{api}', p.test_create()), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('put', f'{api}/{p.id}', updated_p.test_update()), 400)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_sound_notfound(rh, creatable_guest_media, creatable_sound):
    p = creatable_guest_media
    updated_p = Model(creatable_guest_media.id,
                      creatable_guest_media.guest,
                      creatable_guest_media.media,
                      creatable_sound,
                      Color(0xFEDCBA))

    rh.assert_response(rh.open('post', f'{api}', p.test_create()), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('put', f'{api}/{p.id}', updated_p.test_update()), 400)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
