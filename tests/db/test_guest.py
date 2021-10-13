import pytest
import sqlite3
import textwrap


from rfidsecuritysvc.db import guest as db
from rfidsecuritysvc.exception import DuplicateGuestError as Duplicate
from rfidsecuritysvc.exception import GuestNotFoundError as NotFound


def test_get(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                        SELECT
                                        guest.id,
                                        guest.first_name,
                                        guest.last_name,
                                        guest.default_sound,
                                        sound.name as default_sound_name,
                                        guest.default_color
                                        FROM
                                        guest
                                        LEFT JOIN sound on guest.default_sound = sound.id
                                        WHERE guest.id = ?
                                        ORDER BY guest.id
                                        ''').replace('\n', ' '), (1,), 1)
    assert db.get(1) == 1


def test_list(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                        SELECT
                                        guest.id,
                                        guest.first_name,
                                        guest.last_name,
                                        guest.default_sound,
                                        sound.name as default_sound_name,
                                        guest.default_color
                                        FROM
                                        guest
                                        LEFT JOIN sound on guest.default_sound = sound.id
                                        ORDER BY guest.id
                                        ''').replace('\n', ' '), cursor_return=[])
    assert db.list() == []


def test_create(mockdb, default_sound):
    mockdb.add_execute(textwrap.dedent('''
                                 INSERT INTO guest
                                 (first_name, last_name, default_sound, default_color)
                                 VALUES (?,?,?,?)
                                 ''').replace('\n', ' '), ('first', 'last', default_sound.id, 0xABCDEF))
    mockdb.add_commit()
    assert db.create('first', 'last', default_sound.id, 0xABCDEF) is None


def test_create_IntegrityError(mockdb, default_sound):
    mockdb.add_execute(textwrap.dedent('''
                                 INSERT INTO guest
                                 (first_name, last_name, default_sound, default_color)
                                 VALUES (?,?,?,?)
                                 ''').replace('\n', ' '), ('first', 'last', default_sound.id, 0xABCDEF))
    mockdb.add_commit(sqlite3.IntegrityError)
    mockdb.add_rollback()
    with pytest.raises(Duplicate) as e:
        db.create('first', 'last', default_sound.id, 0xABCDEF)

    assert type(e.value.__cause__) == sqlite3.IntegrityError


def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM guest WHERE id = ?', (1,), rowcount=1)
    mockdb.add_commit()
    assert db.delete(1) == 1


def test_update(mockdb, default_sound):
    mockdb.add_execute(textwrap.dedent('''
                                         UPDATE guest
                                         SET first_name = ?, last_name = ?, default_sound = ?, default_color = ?
                                         WHERE id = ?
                                         ''').replace('\n', ' '), ('first', 'last', default_sound.id, 0xABCDEF, 1), rowcount=1)
    mockdb.add_commit()
    assert db.update(1, 'first', 'last', default_sound.id, 0xABCDEF) == 1


def test_update_NotFoundError(mockdb, default_sound):
    mockdb.add_execute(textwrap.dedent('''
                                         UPDATE guest
                                         SET first_name = ?, last_name = ?, default_sound = ?, default_color = ?
                                         WHERE id = ?
                                         ''').replace('\n', ' '), ('first', 'last', default_sound.id, 0xABCDEF, 1), rowcount=0)
    with pytest.raises(NotFound):
        db.update(1, 'first', 'last', default_sound.id, 0xABCDEF)
