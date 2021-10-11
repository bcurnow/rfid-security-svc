from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import guest_media as api
from rfidsecuritysvc.exception import DuplicateGuestMediaError as DuplicateError, GuestMediaNotFoundError as NotFoundError, MediaNotFoundError, GuestNotFoundError, SoundNotFoundError
from rfidsecuritysvc.model.guest_media import GuestMedia as Model
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.sound import Sound

sound = Sound(1, 'test.wav')
guest = Guest(1, 'first_name', 'last_name', sound.id, sound.name, 0xABCDEF)
media = Media('media_id', 'media_name', 'media_desc')
m = Model(1, guest, media, sound.id, sound.name, 0xABCDEF)


@patch('rfidsecuritysvc.api.guest_media.model')
def test_get(model):
    model.get.return_value = m
    assert api.get(m.id) == m.to_json()
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.guest_media.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get(m.id) == (f'Object with id "{m.id}" does not exist.', 404)
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.guest_media.model')
def test_search(model):
    guest2 = Guest(2, 'first_name2', 'last_name2', sound.id, sound.name, 0xABCDEF)
    media2 = Media('media_id2', 'media_name2', 'media_desc2')
    m2 = Model(2, guest2, media2, sound.id, sound.name, 0xABCDEF)
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.guest_media.model')
def test_search_with_guest_id(model):
    media2 = Media('media_id2', 'media_name2', 'media_desc2')
    m2 = Model(2, guest, media2, sound.id, sound.name, 0xABCDEF)
    model.list.return_value = [m, m2]
    assert api.search(1) == [m.to_json(), m2.to_json()]
    model.list.assert_called_once_with(1)


@patch('rfidsecuritysvc.api.guest_media.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.guest_media.model')
def test_post(model):
    model.create.return_value = None
    assert api.post(m.test_create()) == (None, 201)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_post_Duplicate(model):
    model.create.side_effect = DuplicateError
    assert api.post(m.test_create()) == (f'Object with guest_id "{m.guest.id} and media_id "{m.media.id}" already exists.', 409)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_post_GuestNotFoundError(model):
    model.create.side_effect = GuestNotFoundError
    assert api.post(m.test_create()) == (f'No guest found with id "{m.guest.id}".', 400)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_post_MediaNotFoundError(model):
    model.create.side_effect = MediaNotFoundError
    assert api.post(m.test_create()) == (f'No media found with id "{m.media.id}".', 400)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_post_SoundNotFoundError(model):
    model.create.side_effect = SoundNotFoundError
    assert api.post(m.test_create()) == (f'No sound found with id "{m.sound_id}".', 400)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_delete(model):
    model.delete.return_value = 1
    assert api.delete(m.id) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put(model):
    model.update.return_value = 1
    assert api.put(m.id, m.test_create()) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_GuestNotFoundError(model):
    model.update.side_effect = GuestNotFoundError
    assert api.put(m.id, m.test_create()) == (f'No guest found with id "{m.guest.id}".', 400)
    model.update.assert_called_once_with(m.id, **m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_MediaNotFoundError(model):
    model.update.side_effect = MediaNotFoundError
    assert api.put(m.id, m.test_create()) == (f'No media found with id "{m.media.id}".', 400)
    model.update.assert_called_once_with(m.id, **m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_SoundNotFoundError(model):
    model.update.side_effect = SoundNotFoundError
    assert api.put(m.id, m.test_create()) == (f'No sound found with id "{m.sound_id}".', 400)
    model.update.assert_called_once_with(m.id, **m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_not_found(model):
    model.update.side_effect = NotFoundError
    assert api.put(m.id, m.test_create()) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(m.id, **m.test_create())
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_not_found_duplicate(model):
    model.update.side_effect = NotFoundError
    model.create.side_effect = DuplicateError
    assert api.put(m.id, m.test_create()) == (f'Object with guest_id "{m.guest.id} and media_id "{m.media.id}" already exists.', 409,)
    model.update.assert_called_once_with(m.id, **m.test_create())
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_not_found_GuestNotFoundError(model):
    model.update.side_effect = NotFoundError
    model.create.side_effect = GuestNotFoundError
    assert api.put(m.id, m.test_create()) == (f'No guest found with id "{m.guest.id}".', 400,)
    model.update.assert_called_once_with(m.id, **m.test_create())
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_not_found_MediaNotFoundError(model):
    model.update.side_effect = NotFoundError
    model.create.side_effect = MediaNotFoundError
    assert api.put(m.id, m.test_create()) == (f'No media found with id "{m.media.id}".', 400,)
    model.update.assert_called_once_with(m.id, **m.test_create())
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guest_media.model')
def test_put_not_found_SoundNotFoundError(model):
    model.update.side_effect = NotFoundError
    model.create.side_effect = SoundNotFoundError
    assert api.put(m.id, m.test_create()) == (f'No sound found with id "{m.sound_id}".', 400,)
    model.update.assert_called_once_with(m.id, **m.test_create())
    model.create.assert_called_once_with(**m.test_create())
