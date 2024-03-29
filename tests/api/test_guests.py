from unittest.mock import patch

from rfidsecuritysvc.api import RECORD_COUNT_HEADER
from rfidsecuritysvc.api import guests as api
from rfidsecuritysvc.exception import GuestNotFoundError as NotFoundError, DuplicateGuestError as DuplicateError, SoundNotFoundError
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest import Guest as Model
from rfidsecuritysvc.model.sound import Sound

m = Model(1, 'first_name', 'last_name', Sound(1, 'sound_name', '2021-09-25 23:13:25'), Color(0x000000))


@patch('rfidsecuritysvc.api.guests.model')
def test_get(model):
    model.get.return_value = m
    assert api.get(m.id) == m.to_json()
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.guests.model')
def test_get_notfound(model):
    model.get.return_value = None
    assert api.get(m.id) == (f'Object with id "{m.id}" does not exist.', 404)
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.guests.model')
def test_search(model):
    m2 = Model('test2', 'name2', 'desc2')
    model.list.return_value = [m, m2]
    assert api.search() == [m.to_json(), m2.to_json()]
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.guests.model')
def test_search_noresults(model):
    model.list.return_value = []
    assert api.search() == []
    model.list.assert_called_once()


@patch('rfidsecuritysvc.api.guests.model')
def test_post(model):
    model.create.return_value = None
    assert api.post(m.test_create()) == (None, 201)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guests.model')
def test_post_Duplicate(model):
    model.create.side_effect = DuplicateError
    assert api.post(m.test_create()) == (f'Object with first_name "{m.first_name}" and last_name "{m.last_name}" already exists.', 409)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guests.model')
def test_post_SoundNotFoundError(model):
    model.create.side_effect = SoundNotFoundError
    assert api.post(m.test_create()) == (f'Sound with id "{m.sound.id}" does not exist.', 400)
    model.create.assert_called_once_with(**m.test_create())


@patch('rfidsecuritysvc.api.guests.model')
def test_delete(model):
    model.delete.return_value = 1
    assert api.delete(m.id) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.delete.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.api.guests.model')
def test_put(model):
    model.update.return_value = 1
    assert api.put(1, m.test_update()) == (None, 200, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(1, **m.test_update())


@patch('rfidsecuritysvc.api.guests.model')
def test_put_does_not_exist(model):
    model.update.side_effect = NotFoundError
    assert api.put(1, m.test_update()) == (None, 201, {RECORD_COUNT_HEADER: 1})
    model.update.assert_called_once_with(1, **m.test_update())
    model.create.assert_called_once_with(**m.test_update())


@patch('rfidsecuritysvc.api.guests.model')
def test_put_SoundNotFoundError(model):
    model.update.side_effect = SoundNotFoundError
    assert api.put(1, m.test_update()) == (f'Sound with id "{m.sound.id}" does not exist.', 400)
    model.update.assert_called_once_with(1, **m.test_update())


@patch('rfidsecuritysvc.api.guests.model')
def test_put_does_not_exist_SoundNotFound(model):
    model.update.side_effect = NotFoundError
    model.create.side_effect = SoundNotFoundError
    assert api.put(1, m.test_update()) == (f'Sound with id "{m.sound.id}" does not exist.', 400)
    model.update.assert_called_once_with(1, **m.test_update())
    model.create.assert_called_once_with(**m.test_update())
