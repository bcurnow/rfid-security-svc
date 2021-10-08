from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'media'


def test_get(rh, medias):
    rh.assert_response(rh.open('get', f'{api}/{medias[0].id}'), 200, medias[0])


def test_get_no_desc(rh, no_desc_media):
    rh.assert_response(rh.open('get', f'{api}/{no_desc_media.id}'), 200, no_desc_media)


def test_get_notfound(rh, medias):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)


def test_search(rh, medias):
    rh.assert_response(rh.open('get', f'{api}'), 200, medias)


@patch(f'rfidsecuritysvc.api.{api}.model')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_media):
    rh.assert_response(rh.open('post', f'{api}', creatable_media), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_media.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_media.id}'), 404)


def test_post_duplicate(rh, medias):
    rh.assert_response(rh.open('post', f'{api}', medias[0]), 409)


def test_delete(rh, creatable_media):
    rh.assert_response(rh.open('post', f'{api}', creatable_media), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_media.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_media.id}'), 404)


def test_delete_notfound(rh, creatable_media):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media.id}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, medias):
    rh.assert_response(rh.open('put', f'{api}/{medias[0].id}', _update(medias[0])), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_notfound(rh, creatable_media):
    rh.assert_response(rh.open('put', f'{api}/{creatable_media.id}', _update(creatable_media)), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_media.id}', creatable_media), 200, headers={RECORD_COUNT_HEADER: '1'})


def _update(m):
    """
    This is only needed for the Media object because it's the only one that has a non-generated id.
    It can't be marked read-only in the schema because it has to be allowed in the post/create flow.
    So, we need to drop the ID when doing an update.
    """
    json = m.to_json().copy()
    del json['id']
    return json
