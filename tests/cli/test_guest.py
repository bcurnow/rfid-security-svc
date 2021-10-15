import pytest
from unittest.mock import patch

from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.guest import get, create, delete, update
from rfidsecuritysvc.exception import DuplicateGuestError as DuplicateError
from rfidsecuritysvc.exception import GuestNotFoundError as NotFoundError
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest import Guest as Model
from rfidsecuritysvc.model.sound import Sound

c = Color(0xABCDEF)
s = Sound(1, 'sound_name')
m = Model(1, 'first_name', 'last_name', s, c)


@patch('rfidsecuritysvc.cli.guest.model')
def test_get(model, runner, assert_output):
    model.get.return_value = m
    result = runner.invoke(args=['guest', 'get', str(m.id)])
    assert_output(result, m.to_json())
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.cli.guest.model')
def test_get_notfound(model, runner, assert_output):
    model.get.return_value = None
    result = runner.invoke(args=['guest', 'get', str(m.id)], color=True)
    assert_output(result, f'No record found with id "{m.id}".', 2, fg='red')
    model.get.assert_called_once_with(m.id)


def test_get_id_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: id'):
        get.make_context('guest get', args=[])


@patch('rfidsecuritysvc.cli.guest.model')
def test_list(model, runner, assert_output):
    m2 = Model('id2', 'name2', 'desc2')
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['guest', 'list'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.guest.model')
def test_create(model, runner, assert_output):
    model.create.return_value = None
    model.list.return_value = [m]
    result = runner.invoke(args=['guest', 'create', m.first_name, m.last_name, str(m.sound.id), str(m.color.int)])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.first_name, m.last_name, m.sound.id, m.color.int)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.guest.model')
def test_create_duplicate(model, runner, assert_output):
    model.create.side_effect = DuplicateError
    result = runner.invoke(args=['guest', 'create', m.first_name, m.last_name, str(m.sound.id), str(m.color.int)], color=True)
    assert_output(result, f'Record with first_name "{m.first_name}" and last_name "{m.last_name}" already exists.', 2, fg='red')
    model.create.assert_called_once_with(m.first_name, m.last_name, m.sound.id, m.color.int)


def test_create_first_name_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: first_name'):
        create.make_context('guest create', args=[])


def test_create_last_name_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: last_name'):
        create.make_context('guest create', args=[m.first_name])


@patch('rfidsecuritysvc.cli.guest.model')
def test_create_optional(model, runner, assert_output):
    model.create.return_value = None
    model.list.return_value = [m]
    result = runner.invoke(args=['guest', 'create', m.first_name, m.last_name])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.first_name, m.last_name, None, None)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.guest.model')
def test_delete(model, runner, assert_output):
    model.delete.return_value = 1
    result = runner.invoke(args=['guest', 'delete', str(m.id)], color=True)
    assert_output(result, '1 record(s) deleted.', bg='green', fg='black')
    model.delete.assert_called_once_with(m.id)


def test_delete_id_required():
    with pytest.raises(MissingParameter):
        delete.make_context('guest delete', args=[])


@patch('rfidsecuritysvc.cli.guest.model')
def test_update(model, runner, assert_output):
    model.update.return_value = 1
    model.list.return_value = [m]
    result = runner.invoke(args=['guest', 'update', str(m.id), m.first_name, m.last_name, str(m.sound.id), str(m.color.int)], color=True)
    assert_output(result, 'Record updated.', bg='green', fg='black')
    model.update.assert_called_once_with(m.id, m.first_name, m.last_name, m.sound.id, m.color.int)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.guest.model')
def test_update_notfound(model, runner, assert_output):
    model.update.side_effect = NotFoundError
    result = runner.invoke(args=['guest', 'update', str(m.id), m.first_name, m.last_name, str(m.sound.id), str(m.color.int)], color=True)
    assert_output(result, f'Record with id "{m.id}" does not exist.', 2, fg='red')
    model.update.assert_called_once_with(m.id, m.first_name, m.last_name, m.sound.id, m.color.int)


def test_update_id_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: id'):
        update.make_context('guest update', args=[])


def test_update_first_name_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: first_name'):
        update.make_context('guest update', args=['1'])


def test_update_last_name_required():
    with pytest.raises(MissingParameter, match='[M|m]issing parameter: last_name'):
        update.make_context('guest update', args=['1', m.first_name])
