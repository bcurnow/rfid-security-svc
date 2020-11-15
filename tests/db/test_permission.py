import pytest
import sqlite3

from rfidsecuritysvc.db import permission as db
from rfidsecuritysvc.exception import DuplicatePermissionError as Duplicate
from rfidsecuritysvc.exception import PermissionNotFoundError as NotFound


def test_get(mockdb):
    mockdb.add_execute('SELECT * FROM permission WHERE id = ?', ('test',), 'test')
    assert db.get('test') == 'test'


def test_get_by_name(mockdb):
    mockdb.add_execute('SELECT * FROM permission WHERE name = ?', ('test',), 'test')
    assert db.get_by_name('test') == 'test'


def test_list(mockdb):
    mockdb.add_execute('SELECT * FROM permission ORDER BY id', cursor_return=[])
    assert db.list() == []


def test_create(mockdb):
    mockdb.add_execute('INSERT INTO permission (name, desc) VALUES (?,?)', ('test name', 'test desc'))
    mockdb.add_commit()
    assert db.create('test name', 'test desc') is None


def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO permission (name, desc) VALUES (?,?)', ('test name', 'test desc'))
    mockdb.add_commit(sqlite3.IntegrityError)
    mockdb.add_rollback()
    with pytest.raises(Duplicate) as e:
        db.create('test name', 'test desc')

    assert type(e.value.__cause__) == sqlite3.IntegrityError


def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM permission WHERE id = ?', ('test',), rowcount=1)
    mockdb.add_commit()
    assert db.delete('test') == 1


def test_delete_by_name(mockdb):
    mockdb.add_execute('DELETE FROM permission WHERE name = ?', ('test',), rowcount=1)
    mockdb.add_commit()
    assert db.delete_by_name('test') == 1


def test_update(mockdb):
    mockdb.add_execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', ('test name', 'test desc', 'test'), rowcount=1)
    mockdb.add_commit()
    assert db.update('test', 'test name', 'test desc') == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', ('test name', 'test desc', 'test'), rowcount=0)
    mockdb.add_commit()
    with pytest.raises(NotFound):
        db.update('test', 'test name', 'test desc')


def test_update_by_name(mockdb):
    mockdb.add_execute('UPDATE permission SET desc = ? WHERE name = ?', ('test desc', 'test name'), rowcount=1)
    mockdb.add_commit()
    assert db.update_by_name('test name', 'test desc') == 1


def test_update_by_name_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE permission SET desc = ? WHERE name = ?', ('test desc', 'test name'), rowcount=0)
    mockdb.add_commit()
    with pytest.raises(NotFound):
        db.update_by_name('test name', 'test desc')
