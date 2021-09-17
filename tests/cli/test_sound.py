import pytest
from unittest.mock import patch

from click.exceptions import MissingParameter

from rfidsecuritysvc.cli.sound import get, create, delete, update
from rfidsecuritysvc.exception import DuplicateSoundError as DuplicateError
from rfidsecuritysvc.exception import SoundNotFoundError as NotFoundError
from rfidsecuritysvc.model.sound import Sound as Model

m = Model('id', 'file_name')


@patch('rfidsecuritysvc.cli.sound.model')
def test_get(model, runner, assert_output):
    model.get.return_value = m
    result = runner.invoke(args=['sound', 'get', m.id])
    assert_output(result, m.to_json())
    model.get.assert_called_once_with(m.id)


@patch('rfidsecuritysvc.cli.sound.model')
def test_get_notfound(model, runner, assert_output):
    model.get.return_value = None
    result = runner.invoke(args=['sound', 'get', m.id], color=True)
    assert_output(result, f'No record found with id "{m.id}".', 2, fg='red')
    model.get.assert_called_once_with(m.id)


def test_get_id_required():
    with pytest.raises(MissingParameter, match='Missing parameter: id'):
        get.make_context('sound get', args=[])


@patch('rfidsecuritysvc.cli.sound.model')
def test_list(model, runner, assert_output):
    m2 = Model('id2', 'file_name2')
    model.list.return_value = [m, m2]
    result = runner.invoke(args=['sound', 'list'])
    assert_output(result, m.to_json())
    assert_output(result, m2.to_json())
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.sound.model')
def test_create(model, runner, assert_output, tmp_path):
    model.create.return_value = None
    model.list.return_value = [m]
    f = tmp_path / "binary.file"
    f.touch()
    result = runner.invoke(args=['sound', 'create', m.file_name, str(f)])
    assert_output(result, m.to_json())
    model.create.assert_called_once_with(m.file_name, b'')
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.sound.model')
def test_create_duplicate(model, runner, assert_output, tmp_path):
    model.create.side_effect = DuplicateError
    f = tmp_path / "binary.file"
    f.touch()
    result = runner.invoke(args=['sound', 'create', m.file_name, str(f)], color=True)
    assert_output(result, f'Record with file name "{m.file_name}" already exists.', 2, fg='red')
    model.create.assert_called_once_with(m.file_name, b'')


def test_create_file_name_required():
    with pytest.raises(MissingParameter, match='Missing parameter: file_name'):
        create.make_context('sound create', args=[])


def test_create_input_file_required():
    with pytest.raises(MissingParameter, match='Missing parameter: input_file'):
        create.make_context('sound create', args=[m.file_name])


@patch('rfidsecuritysvc.cli.sound.model')
def test_delete(model, runner, assert_output):
    model.delete.return_value = 1
    result = runner.invoke(args=['sound', 'delete', m.id], color=True)
    assert_output(result, '1 record(s) deleted.', bg='green', fg='black')
    model.delete.assert_called_once_with(m.id)


def test_delete_id_required():
    with pytest.raises(MissingParameter, match='Missing parameter: id'):
        delete.make_context('sound delete', args=[])


@patch('rfidsecuritysvc.cli.sound.model')
def test_update(model, runner, assert_output):
    model.update.return_value = 1
    model.list.return_value = [m]
    result = runner.invoke(args=['sound', 'update', m.id, m.file_name], color=True)
    assert_output(result, 'Record updated.', bg='green', fg='black')
    model.update.assert_called_once_with(m.id, m.file_name)
    model.list.assert_called_once()


@patch('rfidsecuritysvc.cli.sound.model')
def test_update_notfound(model, runner, assert_output):
    model.update.side_effect = NotFoundError
    result = runner.invoke(args=['sound', 'update', m.id, m.file_name], color=True)
    assert_output(result, f'Record with id "{m.id}" does not exist.', 2, fg='red')
    model.update.assert_called_once_with(m.id, m.file_name)


def test_update_id_required():
    with pytest.raises(MissingParameter, match='Missing parameter: id'):
        update.make_context('sound update', args=[])


def test_update_file_name_required():
    with pytest.raises(MissingParameter, match='Missing parameter: file_name'):
        update.make_context('sound update', args=[m.id])
