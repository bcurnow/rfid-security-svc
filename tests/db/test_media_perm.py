import pytest
import sqlite3
import textwrap

from rfidsecuritysvc.db import media_perm as db
from rfidsecuritysvc.exception import DuplicateMediaPermError as Duplicate
from rfidsecuritysvc.exception import MediaPermNotFoundError as NotFound


def test_get(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       media_perm.id,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       permission_id,
                                       permission.name as permission_name,
                                       permission.desc as permission_desc
                                       FROM
                                       media_perm
                                       INNER JOIN media on media.id = media_perm.media_id
                                       INNER JOIN permission ON permission.id = media_perm.permission_id
                                       WHERE media_perm.id = ?
                                       ORDER BY media_perm.id
                                       ''').replace('\n', ' '), ('test',), 'test')
    assert db.get('test') == 'test'


def test_get_by_media_and_perm(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       media_perm.id,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       permission_id,
                                       permission.name as permission_name,
                                       permission.desc as permission_desc
                                       FROM
                                       media_perm
                                       INNER JOIN media on media.id = media_perm.media_id
                                       INNER JOIN permission ON permission.id = media_perm.permission_id
                                       WHERE media_perm.media_id = ? AND permission.name = ?
                                       ORDER BY media_perm.id
                                       ''').replace('\n', ' '), ('test', 1), 'test')
    assert db.get_by_media_and_perm('test', 1) == 'test'


def test_list(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       media_perm.id,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       permission_id,
                                       permission.name as permission_name,
                                       permission.desc as permission_desc
                                       FROM
                                       media_perm
                                       INNER JOIN media on media.id = media_perm.media_id
                                       INNER JOIN permission ON permission.id = media_perm.permission_id
                                       ORDER BY media_perm.id
                                       ''').replace('\n', ' '), cursor_return=[])
    assert db.list() == []


def test_list_with_media_id(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       media_perm.id,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       permission_id,
                                       permission.name as permission_name,
                                       permission.desc as permission_desc
                                       FROM
                                       media_perm
                                       INNER JOIN media on media.id = media_perm.media_id
                                       INNER JOIN permission ON permission.id = media_perm.permission_id
                                       WHERE media_id = ?
                                       ORDER BY media_perm.id
                                       ''').replace('\n', ' '), ('test',), cursor_return=[])
    assert db.list('test') == []


def test_create(mockdb):
    mockdb.add_execute('INSERT INTO media_perm (media_id, permission_id) VALUES (?,?)', ('test', 1))
    mockdb.add_commit()
    assert db.create('test', 1) is None


def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO media_perm (media_id, permission_id) VALUES (?,?)', ('test', 1))
    mockdb.add_commit(sqlite3.IntegrityError)
    mockdb.add_rollback()
    with pytest.raises(Duplicate) as e:
        db.create('test', 1)

    assert type(e.value.__cause__) == sqlite3.IntegrityError


def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM media_perm WHERE id = ?', ('test',), rowcount=1)
    mockdb.add_commit()
    assert db.delete('test') == 1


def test_update(mockdb):
    mockdb.add_execute('UPDATE media_perm SET media_id = ?, permission_id = ? WHERE id = ?', ('test', 1, 2), rowcount=1)
    mockdb.add_commit()
    assert db.update(2, 'test', 1) == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute('UPDATE media_perm SET media_id = ?, permission_id = ? WHERE id = ?', ('test', 1, 2), rowcount=0)
    mockdb.add_commit()
    with pytest.raises(NotFound):
        db.update(2, 'test', 1)
