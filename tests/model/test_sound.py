import base64
from datetime import datetime, timezone
from unittest.mock import patch

import rfidsecuritysvc.model.sound as model
from rfidsecuritysvc.model.sound import Sound


def test_Sound(assert_model):
    dt = datetime.now().isoformat(timespec='seconds')
    assert_model(_model('id', 'name', dt, 'binary content'), Sound('id', 'name', dt, 'binary content'))
    assert_model(_model('id', 'name', dt), Sound('id', 'name', dt))


def test_Sound_to_json(assert_model):
    json = Sound(1, 'name', '2021-09-25 23:13:25').to_json()
    assert_model(json, {'id': 1, 'name': 'name', 'last_update_timestamp': '2021-09-25T23:13:25+00:00'})


def test_Sound_to_json_when_content_present(assert_model):
    json = Sound(1, 'name', None, 'binary content').to_json()
    assert_model(json, {'id': 1, 'name': 'name'})


def test_Sound_to_json_all_fields(assert_model):
    dt = datetime.now().isoformat(timespec='seconds')
    json = Sound(1, 'name', dt, 'binary content').to_json()
    expected_dt = datetime.fromisoformat(dt)
    expected_dt = expected_dt.replace(tzinfo=timezone.utc)
    assert_model(json, {'id': 1, 'name': 'name', 'last_update_timestamp': expected_dt.isoformat(timespec='seconds')})


def test_Sound_to_json_with_content(assert_model, wav_content):
    json = Sound(1, 'name', '2021-09-25 23:13:25', wav_content).to_json_with_content()
    assert_model(json, {'id': 1, 'name': 'name', 'last_update_timestamp': '2021-09-25T23:13:25+00:00', 'content': base64.b64encode(wav_content).decode('ascii')})


def test_Sound_to_json_with_content_all_fields(assert_model, wav_content):
    json = Sound(1, 'name', '2021-09-25 23:13:25', wav_content).to_json_with_content()
    assert_model(json, {'id': 1,
                        'name': 'name',
                        'content': base64.b64encode(wav_content).decode('ascii'),
                        'last_update_timestamp': '2021-09-25T23:13:25+00:00'})


@patch('rfidsecuritysvc.model.sound.table')
def test_get(table):
    table.get.return_value = _default().test_to_row()
    assert model.get(1) == _default()
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.sound.table')
def test_get_by_name(table):
    table.get_by_name.return_value = _default().test_to_row()
    assert model.get_by_name('test') == _default()
    table.get_by_name.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.sound.table')
def test_get_notfound(table):
    table.get.return_value = None
    assert model.get(1) is None
    table.get.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.sound.table')
def test_list(table):
    table.list.return_value = [
        _default().to_json(),
        _default(2).to_json(),
    ]
    models = model.list()
    table.list.assert_called_once()
    assert models == [_default(), _default(2)]


@patch('rfidsecuritysvc.model.sound.table')
def test_list_noresults(table):
    table.list.return_value = []
    models = model.list()
    table.list.assert_called_once()
    assert models == []


@patch('rfidsecuritysvc.model.sound.table')
def test_create(table):
    table.create.return_value = None
    assert model.create('test', 'binary content') is None
    table.create.assert_called_once_with('test', 'binary content')


@patch('rfidsecuritysvc.model.sound.table')
def test_delete(table):
    table.delete.return_value = 1
    assert model.delete(1) == 1
    table.delete.assert_called_once_with(1)


@patch('rfidsecuritysvc.model.sound.table')
def test_update(table):
    table.update.return_value = 1
    assert model.update(1, 'test', 'binary content') == 1
    table.update.assert_called_once_with(1, 'test', 'binary content')


@patch('rfidsecuritysvc.model.sound.table')
def test_update_no_content(table):
    table.update.return_value = 1
    assert model.update(1, 'test') == 1
    table.update.assert_called_once_with(1, 'test', None)


def _default(index=1):
    return _model(f'test id {index}', f'test name {index}')


def _model(id, name, last_update_timestamp=datetime.now().replace(tzinfo=timezone.utc).isoformat(timespec='seconds'), content=None):
    return Sound(id, name, last_update_timestamp, content)
