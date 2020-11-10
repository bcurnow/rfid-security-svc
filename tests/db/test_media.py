import pytest
import sqlite3

from rfidsecuritysvc.db import media as db
from rfidsecuritysvc.exception import DuplicateMediaError as Duplicate
from rfidsecuritysvc.exception import MediaNotFoundError as NotFound

def test_get(mockdb):
    mockdb.add_execute('SELECT * FROM media WHERE id = ?', ('test',), 'test')
    assert db.get('test') == 'test'

def test_list(mockdb):
    mockdb.add_execute('SELECT * FROM media ORDER BY id', cursor_return=[])
    assert db.list() == []

def test_create(mockdb):
    mockdb.add_execute('INSERT INTO media (id, name, desc) VALUES (?,?,?)', ('test', 'test name', 'test desc'))
    mockdb.add_commit()
    assert db.create('test', 'test name', 'test desc') == None

def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO media (id, name, desc) VALUES (?,?,?)', ('test', 'test name', 'test desc'))
    mockdb.add_commit(sqlite3.IntegrityError)
    with pytest.raises(Duplicate) as e:
        db.create('test', 'test name', 'test desc')

    assert type(e.value.__cause__) == sqlite3.IntegrityError

def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM media WHERE id = ?', ('test',), rowcount=1)
    mockdb.add_commit()
    assert db.delete('test') == 1

def test_update(mockdb):
    mockdb.add_execute('UPDATE media SET name = ?, desc = ? WHERE id = ?', ('test name', 'test desc', 'test'), rowcount=1)
    mockdb.add_commit()
    assert db.update('test', 'test name', 'test desc') == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE media SET name = ?, desc = ? WHERE id = ?', ('test name', 'test desc', 'test'), rowcount=0)
    mockdb.add_commit()
    with pytest.raises(NotFound):
        db.update('test', 'test name', 'test desc')

