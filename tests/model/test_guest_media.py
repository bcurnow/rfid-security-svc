import pytest

from unittest.mock import patch

import rfidsecuritysvc.model.guest_media as model
from rfidsecuritysvc.exception import GuestNotFoundError, MediaNotFoundError, SoundNotFoundError
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.guest_media import GuestMedia
from rfidsecuritysvc.model.media import Media


def test_GuestMedia(assert_model, open_door_guest, open_door_media, default_sound):
    assert_model(_model(1, open_door_guest, open_door_media, default_sound.id, default_sound.name, 0xABCDEF),
                 GuestMedia(1, open_door_guest, open_door_media, default_sound.id, default_sound.name, 0xABCDEF))


def test_GuestMedia_default_color_zero(open_door_guest, open_door_media, default_sound):
    m = GuestMedia(1, open_door_guest, open_door_media, default_sound.id, default_sound.name, 0)
    assert m.color_hex == "0"
    assert m.color_html == "#000000"


def test_GuestMedia_to_json(open_door_guest, open_door_media, default_sound):
    json = GuestMedia(1, open_door_guest, open_door_media, default_sound.id, default_sound.name, 0xABCDEF).to_json()
    assert json['id'] == 1
    assert json['guest'] == open_door_guest.to_json()
    assert json['media'] == open_door_media.to_json()
    assert json['sound_id'] == default_sound.id
    assert json['sound_name'] == default_sound.name
    assert json['color'] == 0xABCDEF
    assert json['color_hex'] == 'ABCDEF'
    assert json['color_html'] == '#abcdef'


@patch('rfidsecuritysvc.model.guest_media.table')
def test_get(table, guest_media_to_row):
    table.get.return_value = guest_media_to_row(_default())
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest_media.table')
def test_get_by_media(table, guest_media_to_row):
    table.get_by_media.return_value = guest_media_to_row(_default())
    assert model.get_by_media('test') == _default()
    table.get_by_media.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.guest_media.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest_media.table')
def test_list(table, guest_media_to_row):
    table.list.return_value = [
        guest_media_to_row(_default()),
        guest_media_to_row(_default(2)),
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.guest_media.table')
def test_list_with_guest_id(table, guest_media_to_row):
    table.list.return_value = [
        guest_media_to_row(_default()),
        guest_media_to_row(_default(2)),
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


@patch('rfidsecuritysvc.model.guest_media.sound')
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


# @patch('rfidsecuritysvc.model.guest_media.table')
# def test_update(table):
#     table.update.return_value = 1
#     assert model.update(1, 'test', 1) == 1
#     table.update.assert_called_once_with(1, 'test', 1)
#
#
def _default(index=1):
    g = Guest(index, f'test guest_first_name {index}', f'test guest_last_name {index}', 1, 'test.wav', 0xABCDEF)
    m = Media(f'test media_id {index}', f'test media_name {index}', f'test media_desc {index}')
    return _model(index, g, m, 1, 'test.wav', 0xABCDEF)


def _model(id, guest, media, sound_id=None, sound_name=None, color=None):
    return GuestMedia(id, guest, media, sound_id, sound_name, color)
