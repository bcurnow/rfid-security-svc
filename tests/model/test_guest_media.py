import pytest

from unittest.mock import patch

import rfidsecuritysvc.model.guest_media as model
from rfidsecuritysvc.exception import GuestNotFoundError, MediaNotFoundError, SoundNotFoundError
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.guest_media import GuestMedia
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.sound import Sound


def test_GuestMedia(assert_model, open_door_guest, open_door_media, default_sound, default_color):
    assert_model(_model(1, open_door_guest, open_door_media, default_sound, default_color),
                 GuestMedia(1, open_door_guest, open_door_media, default_sound, default_color))


def test_GuestMedia_to_json(open_door_guest, open_door_media, default_sound, default_color):
    json = GuestMedia(1, open_door_guest, open_door_media, default_sound, default_color).to_json()
    assert json['id'] == 1
    assert json['guest'] == open_door_guest.to_json()
    assert json['media'] == open_door_media.to_json()
    assert json['sound'] == default_sound.to_json()
    assert json['color'] == default_color.to_json()


@patch('rfidsecuritysvc.model.guest_media.table')
def test_get(table):
    table.get.return_value = _default().test_to_row()
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest_media.table')
def test_get_by_media(table):
    table.get_by_media.return_value = _default().test_to_row()
    assert model.get_by_media('test') == _default()
    table.get_by_media.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.guest_media.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest_media.table')
def test_list(table):
    table.list.return_value = [
        _default().test_to_row(),
        _default(2).test_to_row(),
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.guest_media.table')
def test_list_with_guest_id(table):
    table.list.return_value = [
        _default().test_to_row(),
        _default(2).test_to_row(),
    ]
    models = model.list(1)
    table.list.assert_called_once_with(1)
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.guest_media.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_create(table, guest, media, sound, default_sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = Media('test', 'test')
    sound.get.return_value = default_sound
    table.create.return_value = None
    assert model.create(1, 'test', default_sound.id, 0xABCDEF) is None
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_called_once_with(default_sound.id)
    table.create.assert_called_once_with(1, 'test', default_sound.id, 0xABCDEF)


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_create_no_prefs(table, guest, media, sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = Media('test', 'test')
    table.create.return_value = None
    assert model.create(1, 'test', None, None) is None
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_not_called()
    table.create.assert_called_once_with(1, 'test', None, None)


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_create_no_guest(table, guest, media, sound):
    guest.get.return_value = None
    with pytest.raises(GuestNotFoundError):
        model.create(1, 'test', None, None)
    guest.get.assert_called_once_with(1)
    media.get.assert_not_called()
    sound.get.assert_not_called()
    table.create.assert_not_called()


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_create_no_media(table, guest, media, sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = None
    with pytest.raises(MediaNotFoundError):
        model.create(1, 'test', None, None)
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_not_called()
    table.create.assert_not_called()


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_create_no_sound(table, guest, media, sound, default_sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = Media('test', 'test')
    sound.get.return_value = None
    with pytest.raises(SoundNotFoundError):
        model.create(1, 'test', default_sound.id, None) is None
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_called_once_with(default_sound.id)
    table.create.assert_not_called()


@patch('rfidsecuritysvc.model.guest_media.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_with(1)


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_update(table, guest, media, sound, default_sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = Media('test', 'test')
    sound.get.return_value = default_sound
    table.update.return_value = None
    assert model.update(1, 1, 'test', default_sound.id, 0xABCDEF) is None
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_called_once_with(default_sound.id)
    table.update.assert_called_once_with(1, 1, 'test', default_sound.id, 0xABCDEF)


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_update_no_sound(table, guest, media, sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = Media('test', 'test')
    table.update.return_value = None
    assert model.update(1, 1, 'test', None, 0xABCDEF) is None
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_not_called()
    table.update.assert_called_once_with(1, 1, 'test', None, 0xABCDEF)


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_update_SoundNotFoundError(table, guest, media, sound, default_sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = Media('test', 'test')
    sound.get.return_value = None
    with pytest.raises(SoundNotFoundError):
        model.update(1, 1, 'test', default_sound.id, 0xABCDEF)
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_called_once_with(default_sound.id)
    table.update.assert_not_called()


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_update_MediaNotFoundError(table, guest, media, sound, default_sound):
    guest.get.return_value = Guest(1, 'first_name', 'last_name')
    media.get.return_value = None
    with pytest.raises(MediaNotFoundError):
        model.update(1, 1, 'test', default_sound.id, 0xABCDEF)
    guest.get.assert_called_once_with(1)
    media.get.assert_called_once_with('test')
    sound.get.assert_not_called()
    table.update.assert_not_called()


@patch('rfidsecuritysvc.model.guest_media.soundModel')
@patch('rfidsecuritysvc.model.guest_media.media')
@patch('rfidsecuritysvc.model.guest_media.guest')
@patch('rfidsecuritysvc.model.guest_media.table')
def test_update_GuestNotFoundError(table, guest, media, sound, default_sound):
    guest.get.return_value = None
    with pytest.raises(GuestNotFoundError):
        model.update(1, 1, 'test', default_sound.id, 0xABCDEF)
    guest.get.assert_called_once_with(1)
    media.get.assert_not_called()
    sound.get.assert_not_called()
    table.update.assert_not_called()


def test__model_no_guest_color(creatable_guest_media):
    row = creatable_guest_media.test_to_row()
    row['guest_color'] = None
    gm = model.__model(row)
    assert gm.guest.color is None


def test__model_no_guest_sound(creatable_guest_media):
    row = creatable_guest_media.test_to_row()
    row['guest_sound'] = None
    gm = model.__model(row)
    assert gm.guest.sound is None


def test__model_no_color(creatable_guest_media):
    row = creatable_guest_media.test_to_row()
    row['color'] = None
    gm = model.__model(row)
    assert gm.color is None


def test__model_no_sound(creatable_guest_media):
    row = creatable_guest_media.test_to_row()
    row['sound'] = None
    gm = model.__model(row)
    assert gm.sound is None


def _default(index=1):
    s = Sound(1, 'test.wav', '2021-09-25 23:13:25')
    c = Color(0xABCDEF)
    g = Guest(index, f'test guest_first_name {index}', f'test guest_last_name {index}', s, c)
    m = Media(f'test media_id {index}', f'test media_name {index}', f'test media_desc {index}')
    return _model(index, g, m, s, c)


def _model(id, guest, media, sound=None, color=None):
    return GuestMedia(id, guest, media, sound, color)
