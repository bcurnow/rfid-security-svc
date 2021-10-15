import pytest
from unittest.mock import patch

import rfidsecuritysvc.model.guest as model
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.sound import Sound
from rfidsecuritysvc.exception import SoundNotFoundError


def test_Guest(assert_model, default_sound, default_color):
    assert_model(_model(1, 'first', 'last', default_sound, default_color),
                 Guest(1, 'first', 'last', default_sound, default_color))


@patch('rfidsecuritysvc.model.guest.table')
def test_get(table):
    table.get.return_value = _default().test_to_row()
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.guest.table')
def test_list(table):
    table.list.return_value = [
        _default().test_to_row(),
        _default(2).test_to_row(),
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.guest.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.guest.sound_model')
@patch('rfidsecuritysvc.model.guest.table')
def test_create(table, sound, default_sound):
    sound.get.return_value = default_sound
    table.create.return_value = None
    assert model.create('first', 'last', default_sound.id, 0xABCDEF) is None
    sound.get.assert_called_once_with(default_sound.id)
    table.create.assert_called_once_with('first', 'last', default_sound.id, 0xABCDEF)


@patch('rfidsecuritysvc.model.guest.sound_model')
@patch('rfidsecuritysvc.model.guest.table')
def test_create_SoundNotFoundError(table, sound, default_sound):
    sound.get.return_value = None
    with pytest.raises(SoundNotFoundError):
        model.create('first', 'last', default_sound.id, 0xABCDEF)
    sound.get.assert_called_once_with(default_sound.id)
    table.create.assert_not_called()


@patch('rfidsecuritysvc.model.guest.sound_model')
@patch('rfidsecuritysvc.model.guest.table')
def test_create_no_prefs(table, sound, default_sound):
    table.create.return_value = None
    assert model.create('first', 'last', None, None) is None
    sound.get.assert_not_called()
    table.create.assert_called_once_with('first', 'last', None, None)


@patch('rfidsecuritysvc.model.guest.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_with(1)


@patch('rfidsecuritysvc.model.guest.sound_model')
@patch('rfidsecuritysvc.model.guest.table')
def test_update(table, sound, default_sound):
    sound.get.return_value = default_sound
    table.update.return_value = 1
    assert model.update(1, 'first', 'last', default_sound.id, 0xABCDEF) == 1
    sound.get.assert_called_once_with(default_sound.id)
    table.update.assert_called_once_with(1, 'first', 'last', default_sound.id, 0xABCDEF)


@patch('rfidsecuritysvc.model.guest.sound_model')
@patch('rfidsecuritysvc.model.guest.table')
def test_update_no_prefs(table, sound, default_sound):
    table.update.return_value = 1
    assert model.update(1, 'first', 'last', None, None) == 1
    sound.get.assert_not_called()
    table.update.assert_called_once_with(1, 'first', 'last', None, None)


@patch('rfidsecuritysvc.model.guest.sound_model')
@patch('rfidsecuritysvc.model.guest.table')
def test_update_SoundNotFoundError(table, sound, default_sound):
    table.update.return_value = 1
    sound.get.return_value = None
    with pytest.raises(SoundNotFoundError):
        model.update(1, 'first', 'last', default_sound.id, 0xABCDEF)
    sound.get.assert_called_once_with(default_sound.id)
    table.update.assert_not_called()


def test__model_no_color(creatable_guest):
    row = creatable_guest.test_to_row()
    row['color'] = None
    g = model.__model(row)
    assert g.color is None


def test__model_no_sound(creatable_guest):
    row = creatable_guest.test_to_row()
    row['sound'] = None
    g = model.__model(row)
    assert g.sound is None


def _default(index=1):
    return _model(index, f'first {index}', f'last {index}', Sound(index, f'sound_name {index}', '2021-09-25 23:13:25'), Color(0xABCDEF))


def _model(id, first_name, last_name, sound, color):
    return Guest(id, first_name, last_name, sound, color)
