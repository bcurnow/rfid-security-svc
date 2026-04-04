from io import BytesIO
from unittest.mock import patch

from werkzeug.datastructures import FileStorage

from rfidsecuritysvc.api import RECORD_COUNT_HEADER

api = 'sounds'


def test_get(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/{sounds[0].id}'), 200, sounds[0].to_json_with_content())


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


def test_post(rh, creatable_sound):
    rh.assert_response(rh.open('post', f'{api}', creatable_sound.test_to_multipart(), 'multipart/form-data'), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.id}'), 404)


def test_post_no_content(rh):
    # This will return a 415 (Invalid Content-type) rather than a 400 (Bad Request) as the lack of file information means
    # the Content-Type header will be set to multipart/x-www-form-urlencoded which isn't valid for this endpoint
    rh.assert_response(rh.open('post', f'{api}', ({'name': 'test.wav'}, None), 'multipart/form-data'), 415)


def test_post_wrong_content_type(rh, creatable_sound):
    rh.assert_response(rh.open('post', f'{api}', creatable_sound.test_to_multipart('application/wrong'), 'multipart/form-data'), 415)


def test_post_wrong_missing_name(rh, creatable_sound):
    content = creatable_sound.test_to_multipart()
    content = (None, content[1])  # Remove the form data, leaving just the file information
    # This will return a 415 and not a 400 because the endpoint will reject the request before it
    # checks for the name due to the missing form data meaning that the content type will be set to multipart/x-www-form-urlencoded which isn't valid for this endpoint
    rh.assert_response(rh.open('post', f'{api}', content, 'application/wrong'), 415)


def test_post_duplicate(rh, sounds):
    rh.assert_response(rh.open('post', f'{api}', sounds[0].test_to_multipart(), 'multipart/form-data'), 409)


def test_post_too_little_content(rh, sounds):
    content = sounds[0].test_to_multipart()
    content = (content[0], FileStorage(BytesIO(b''), 'local file name.wav', sounds[0].name, 'audio/wav', 0))  # Replace the file information with an empty file
    rh.assert_response(rh.open('post', f'{api}', content, 'multipart/form-data'), 400)


def test_delete(rh, creatable_sound):
    rh.assert_response(rh.open('post', f'{api}', creatable_sound.test_to_multipart(), 'multipart/form-data'), 201)
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.id}'), 200)
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.id}'), 200, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('get', f'{api}/{creatable_sound.id}'), 404)


def test_delete_notfound(rh, creatable_sound):
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.id}'), 200, headers={RECORD_COUNT_HEADER: '0'})


def test_put(rh, sounds):
    rh.assert_response(rh.open('put', f'{api}/{sounds[0].id}', sounds[0].test_to_multipart(), 'multipart/form-data'), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_no_content(rh, sounds):
    rh.assert_response(
        rh.open(
            'put',
            f'{api}/{sounds[0].id}',
            ({'name': 'rename.wav'}, None),
            'multipart/form-data'
            ),
        415,
        )


def test_put_too_little_content(rh, sounds):
    content = sounds[0].test_to_multipart()
    content = (content[0], FileStorage(BytesIO(b''), 'local file name.wav', sounds[0].name, 'audio/wav', 0))  # Replace the file information with an empty file
    rh.assert_response(
        rh.open(
            'put',
            f'{api}/{sounds[0].id}',
            content,
            'multipart/form-data'
            ),
        400)


def test_put_missing_name(rh, sounds):
    content = sounds[0].test_to_multipart()
    content = (None, content[1])  # Remove the form data, leaving just the file information
    rh.assert_response(
        rh.open(
            'put',
            f'{api}/{sounds[0].id}',
            content,
            'multipart/form-data'
            ),
        400)


def test_put_notfound(rh, creatable_sound):
    rh.assert_response(rh.open('put',
                               f'{api}/{creatable_sound.id}',
                               creatable_sound.test_to_multipart(),
                               'multipart/form-data'
                               ), 201, headers={RECORD_COUNT_HEADER: '1'})
    rh.assert_response(rh.open('delete', f'{api}/{creatable_sound.id}', creatable_sound), 200, headers={RECORD_COUNT_HEADER: '1'})


def test_put_wrong_content_type(rh, creatable_sound):
    rh.assert_response(rh.open('put',
                               f'{api}/{creatable_sound.id}',
                               creatable_sound.test_to_multipart('application/wrong'),
                               'multipart/form-data'
                               ), 415)
