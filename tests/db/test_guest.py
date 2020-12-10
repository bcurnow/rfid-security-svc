import pytest
import sqlite3

from rfidsecuritysvc.db import guest as db
from rfidsecuritysvc.exception import DuplicateGuestError as Duplicate
from rfidsecuritysvc.exception import GuestNotFoundError as NotFound


def test_get(mockdb):
    mockdb.add_execute('SELECT * FROM guest WHERE id = ?', (1,), 1)
    assert db.get(1) == 1


def test_list(mockdb):
    mockdb.add_execute('SELECT * FROM guest ORDER BY id', cursor_return=[])
    assert db.list() == []


def test_create(mockdb):
    mockdb.add_execute('INSERT INTO guest (first_name, last_name) VALUES (?,?)', ('first', 'last'))
    mockdb.add_commit()
    assert db.create('first', 'last') is None


def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO guest (first_name, last_name) VALUES (?,?)', ('first', 'last'))
    mockdb.add_commit(sqlite3.IntegrityError)
    mockdb.add_rollback()
    with pytest.raises(Duplicate) as e:
        db.create('first', 'last')

    assert type(e.value.__cause__) == sqlite3.IntegrityError


def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM guest WHERE id = ?', (1,), rowcount=1)
    mockdb.add_commit()
    assert db.delete(1) == 1


def test_update(mockdb):
    mockdb.add_execute('UPDATE guest SET first_name = ?, last_name = ? WHERE id = ?', ('first', 'last', 1), rowcount=1)
    mockdb.add_commit()
    assert db.update(1, 'first', 'last') == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE guest SET first_name = ?, last_name = ? WHERE id = ?', ('first', 'last', 1), rowcount=0)
    with pytest.raises(NotFound):
        db.update(1, 'first', 'last')
