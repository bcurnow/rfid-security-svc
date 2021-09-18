from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'associations'


def test_get(rh, by_media_associations):
    rh.assert_response(rh.open('get', f'{api}/{by_media_associations[0].media_id}'), 200, by_media_associations)


def test_search(rh, associations):
    rh.assert_response(rh.open('get', f'{api}'), 200, associations)


@patch(f'rfidsecuritysvc.api.{api}.association')
def test_search_noresults(model, rh):
    """ The table is already populated so we need to patch instead """
    model.list.return_value = []
    rh.assert_response(rh.open('get', f'{api}'), 200, [])
    model.list.assert_called_once()


def test_post(rh, creatable_association):
    a = creatable_association
    rh.assert_response(rh.open('post', f'{api}', a), 201)
    rh.assert_response(rh.open('post', f'{api}', a), 409)
    rh.assert_response(rh.open('delete', f'{api}/{a.media_id}/{a.perm_name}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{a.media_id}/{a.perm_name}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_post_duplicate(rh, associations):
    rh.assert_response(rh.open('post', f'{api}', associations[0]), 409)


def test_delete(rh, creatable_association):
    a = creatable_association
    rh.assert_response(rh.open('post', f'{api}', a), 201)
    rh.assert_response(rh.open('post', f'{api}', a), 409)
    rh.assert_response(rh.open('delete', f'{api}/{a.media_id}/{a.perm_name}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{a.media_id}/{a.perm_name}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_delete_notfound(rh, creatable_association):
    a = creatable_association
    rh.assert_response(rh.open('delete', f'{api}/{a.media_id}/{a.perm_name}'), 200, headers={RECORD_COUNT_HEADER: '0'})
