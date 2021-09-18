from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model.media_perm import MediaPerm as Model

api = 'media-perms'


def test_get(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}/{media_perms[0].media_id}/{media_perms[0].perm_id}'), 200, media_perms[0])


def test_get_notfound(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}'), 200, media_perms)


@patch('rfidsecuritysvc.api.media_perms.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_media_perm):
    p = creatable_media_perm
    rh.assert_response(rh.open('post', f'{api}', p), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.media_id}/{p.perm_id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{p.media_id}/{p.perm_id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.media_id}/{p.perm_id}'), 404)


def test_post_duplicate(rh, media_perms):
    rh.assert_response(rh.open('post', f'{api}', media_perms[0]), 409)


def test_post_media_notfound(rh, creatable_media_perm, permissions):
    p = Model(creatable_media_perm.id, 'test_post_media_notfound', permissions[1].id)
    rh.assert_response(rh.open('post', f'{api}', p), 400)


def test_post_permission_notfound(rh, creatable_media_perm, permissions):
    p = Model(creatable_media_perm.id, creatable_media_perm.media_id, len(permissions) * 100)
    rh.assert_response(rh.open('post', f'{api}', p), 400)


def test_delete(rh, creatable_media_perm):
    p = creatable_media_perm
    rh.assert_response(rh.open('post', f'{api}', p), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.media_id}/{p.perm_id}'), 200)
    rh.assert_response(
        rh.open('delete', f'{api}/{p.media_id}/{p.perm_id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.media_id}/{p.perm_id}'), 404)


def test_delete_notfound(rh, creatable_media_perm, permissions):
    p = Model(creatable_media_perm.id, 'test_delete_notfound', permissions[3].id)
    rh.assert_response(rh.open('delete', f'{api}/{p.media_id}/{p.perm_id}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put_create(rh, creatable_media_perm):
    rh.assert_response(rh.open('put', f'{api}/{creatable_media_perm.media_id}/{creatable_media_perm.perm_id}',
                               creatable_media_perm), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media_perm.media_id}/{creatable_media_perm.perm_id}',
                               creatable_media_perm), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_duplicate(rh, media_perms):
    rh.assert_response(
        rh.open('put', f'{api}/{media_perms[0].media_id}/{media_perms[0].perm_id}', media_perms[0]),
        200,
        headers={RECORD_COUNT_HEADER: '0'}
    )
