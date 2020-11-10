import pytest
import sqlite3

from rfidsecuritysvc.db import config as db
from rfidsecuritysvc.exception import DuplicateConfigError as Duplicate
from rfidsecuritysvc.exception import ConfigNotFoundError as NotFound

def test_get(mockdb):
    mockdb.add_execute('SELECT * FROM config WHERE key = ?', ('test',), 'test')
    assert db.get('test') == 'test'

def test_list(mockdb):
    mockdb.add_execute('SELECT * FROM config ORDER BY key', cursor_return=[])
    assert db.list() == []

def test_create(mockdb):
    mockdb.add_execute('INSERT INTO config (key, value) VALUES (?,?)', ('test', 1))
    mockdb.add_commit()
    assert db.create('test', 1) == None

def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO config (key, value) VALUES (?,?)', ('test', 1))
    mockdb.add_commit(sqlite3.IntegrityError)
    with pytest.raises(Duplicate) as e:
        db.create('test', 1)

    assert type(e.value.__cause__) == sqlite3.IntegrityError

def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM config WHERE key = ?', ('test',), rowcount=1)
    mockdb.add_commit()
    assert db.delete('test') == 1

def test_update(mockdb):
    mockdb.add_execute('UPDATE config SET value = ? WHERE key = ?', (1, 'test'), rowcount=1)
    mockdb.add_commit()
    assert db.update('test', 1) == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE config SET value = ? WHERE key = ?', (1, 'test'), rowcount=0)
    mockdb.add_commit()
    with pytest.raises(NotFound):
        db.update('test', 1)
