from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.media_perm import MediaPerm as Model
from rfidsecuritysvc.model.permission import Permission

api = 'media-perms'


def test_get(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}/{media_perms[0].id}'), 200, media_perms[0])


def test_get_notfound(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}'), 200, media_perms)


def test_search_with_media_id(rh, media_perms):
    rh.assert_response(rh.open('get', f'{api}?media_id={media_perms[0].media.id}'), 200, [media_perms[0]])


@patch('rfidsecuritysvc.api.media_perms.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_media_perm):
    p = creatable_media_perm
    rh.assert_response(rh.open('post', f'{api}', p), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 404)


def test_post_duplicate(rh, media_perms):
    rh.assert_response(rh.open('post', f'{api}', media_perms[0]), 409)


def test_post_media_notfound(rh, creatable_media_perm):
    media = Media(**creatable_media_perm.media.test_create())
    permission = Permission(creatable_media_perm.permission.id, **creatable_media_perm.permission.test_create())
    m = Model(creatable_media_perm.id, media, permission)
    media.id = 'bogus'
    rh.assert_response(rh.open('post', f'{api}', m), 400)


def test_post_permission_notfound(rh, creatable_media_perm, permissions):
    media = Media(**creatable_media_perm.media.test_create())
    permission = Permission(creatable_media_perm.permission.id, **creatable_media_perm.permission.test_create())
    m = Model(creatable_media_perm.id, media, permission)
    m.media = media
    m.permission = permission
    permission.id = len(permissions) * 1000
    rh.assert_response(rh.open('post', f'{api}', m), 400)


def test_delete(rh, creatable_media_perm):
    p = creatable_media_perm
    rh.assert_response(rh.open('post', f'{api}', p), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 404)


def test_delete_notfound(rh, creatable_media_perm):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media_perm.id}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, creatable_media_perm, medias, permissions):
    p = creatable_media_perm
    assert p.media.id != medias[2].id
    assert p.permission.id != permissions[2].id
    updated_p = Model(creatable_media_perm.id, medias[2], permissions[2])
    rh.assert_response(rh.open('post', f'{api}', p), 201)
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200)
    rh.assert_response(rh.open('put', f'{api}/{p.id}', updated_p), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200, updated_p)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media_perm.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_not_found(rh, creatable_media_perm, medias, permissions):
    p = creatable_media_perm

    rh.assert_response(rh.open('put', f'{api}/{p.id}', p), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{p.id}'), 200, p)
    rh.assert_response(rh.open('delete', f'{api}/{p.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
