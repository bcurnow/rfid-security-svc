import pytest
import sqlite3

from rfidsecuritysvc.db import sound as db
from rfidsecuritysvc.exception import DuplicateSoundError as Duplicate
from rfidsecuritysvc.exception import SoundNotFoundError as NotFound


def test_get(mockdb):
    mockdb.add_execute('SELECT * FROM sound WHERE id = ?', (1,), 1)
    assert db.get(1) == 1


def test_list(mockdb):
    mockdb.add_execute('SELECT id, name FROM sound ORDER BY id', cursor_return=[])
    assert db.list() == []


def test_create(mockdb):
    mockdb.add_execute('INSERT INTO sound (name, content) VALUES (?,?)', ('test', 'binary content'))
    mockdb.add_commit()
    assert db.create('test', 'binary content') is None


def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO sound (name, content) VALUES (?,?)', ('test', 'binary content'))
    mockdb.add_commit(sqlite3.IntegrityError)
    mockdb.add_rollback()
    with pytest.raises(Duplicate) as e:
        db.create('test', 'binary content')

    assert type(e.value.__cause__) == sqlite3.IntegrityError


def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM sound WHERE id = ?', (1,), rowcount=1)
    mockdb.add_commit()
    assert db.delete(1) == 1


def test_update(mockdb):
    mockdb.add_execute('UPDATE sound SET name = ? WHERE id = ?', (1, 'test'), rowcount=1)
    mockdb.add_commit()
    assert db.update('test', 1) == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE sound SET name = ? WHERE id = ?', (1, 'test'), rowcount=0)
    with pytest.raises(NotFound):
        db.update('test', 1)
