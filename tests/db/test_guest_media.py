import pytest
import sqlite3
import textwrap

from rfidsecuritysvc.db import guest_media as db
from rfidsecuritysvc.exception import DuplicateGuestMediaError as Duplicate
from rfidsecuritysvc.exception import GuestMediaNotFoundError as NotFound


def test_get(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       guest_media.id,
                                       guest_id,
                                       guest.first_name as guest_first_name,
                                       guest.last_name as guest_last_name,
                                       guest.sound as guest_sound,
                                       gs.name as guest_sound_name,
                                       gs.last_update_timestamp as guest_sound_last_update_timestamp,
                                       guest.color as guest_color,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       guest_media.sound as sound_id,
                                       gms.name as sound_name,
                                       gms.last_update_timestamp as sound_last_update_timestamp,
                                       guest_media.color
                                       FROM
                                       guest_media
                                       INNER JOIN media ON media.id = guest_media.media_id
                                       INNER JOIN guest ON guest.id = guest_media.guest_id
                                       LEFT JOIN sound gms ON gms.id = guest_media.sound
                                       LEFT JOIN sound gs ON gs.id = guest.sound
                                       WHERE guest_media.id = ?
                                       ORDER BY guest_media.id
                                       ''').replace('\n', ' '), ('test',), 'test')
    assert db.get('test') == 'test'


def test_get_by_media(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       guest_media.id,
                                       guest_id,
                                       guest.first_name as guest_first_name,
                                       guest.last_name as guest_last_name,
                                       guest.sound as guest_sound,
                                       gs.name as guest_sound_name,
                                       gs.last_update_timestamp as guest_sound_last_update_timestamp,
                                       guest.color as guest_color,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       guest_media.sound as sound_id,
                                       gms.name as sound_name,
                                       gms.last_update_timestamp as sound_last_update_timestamp,
                                       guest_media.color
                                       FROM
                                       guest_media
                                       INNER JOIN media ON media.id = guest_media.media_id
                                       INNER JOIN guest ON guest.id = guest_media.guest_id
                                       LEFT JOIN sound gms ON gms.id = guest_media.sound
                                       LEFT JOIN sound gs ON gs.id = guest.sound
                                       WHERE guest_media.media_id = ?
                                       ORDER BY guest_media.id
                                       ''').replace('\n', ' '), ('test',), 'test')
    assert db.get_by_media('test') == 'test'


def test_list(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       guest_media.id,
                                       guest_id,
                                       guest.first_name as guest_first_name,
                                       guest.last_name as guest_last_name,
                                       guest.sound as guest_sound,
                                       gs.name as guest_sound_name,
                                       gs.last_update_timestamp as guest_sound_last_update_timestamp,
                                       guest.color as guest_color,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       guest_media.sound as sound_id,
                                       gms.name as sound_name,
                                       gms.last_update_timestamp as sound_last_update_timestamp,
                                       guest_media.color
                                       FROM
                                       guest_media
                                       INNER JOIN media ON media.id = guest_media.media_id
                                       INNER JOIN guest ON guest.id = guest_media.guest_id
                                       LEFT JOIN sound gms ON gms.id = guest_media.sound
                                       LEFT JOIN sound gs ON gs.id = guest.sound
                                       ORDER BY guest_media.id
                                        ''').replace('\n', ' '), cursor_return=[])
    assert db.list() == []


def test_list_with_media_id(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       guest_media.id,
                                       guest_id,
                                       guest.first_name as guest_first_name,
                                       guest.last_name as guest_last_name,
                                       guest.sound as guest_sound,
                                       gs.name as guest_sound_name,
                                       gs.last_update_timestamp as guest_sound_last_update_timestamp,
                                       guest.color as guest_color,
                                       media_id,
                                       media.name as media_name,
                                       media.desc as media_desc,
                                       guest_media.sound as sound_id,
                                       gms.name as sound_name,
                                       gms.last_update_timestamp as sound_last_update_timestamp,
                                       guest_media.color
                                       FROM
                                       guest_media
                                       INNER JOIN media ON media.id = guest_media.media_id
                                       INNER JOIN guest ON guest.id = guest_media.guest_id
                                       LEFT JOIN sound gms ON gms.id = guest_media.sound
                                       LEFT JOIN sound gs ON gs.id = guest.sound
                                       WHERE guest_media.guest_id = ?
                                       ORDER BY guest_media.id
                                        ''').replace('\n', ' '), (1,), cursor_return=[])
    assert db.list(1) == []


def test_create(mockdb):
    mockdb.add_execute('INSERT INTO guest_media (guest_id, media_id, sound, color) VALUES (?,?,?,?)', (1, 'test', 1, 0xABCDEF))
    mockdb.add_commit()
    assert db.create(1, 'test', 1, 0xABCDEF) is None


def test_create_IntegrityError(mockdb):
    mockdb.add_execute('INSERT INTO guest_media (guest_id, media_id, sound, color) VALUES (?,?,?,?)', (1, 'test', 1, 0xABCDEF))
    mockdb.add_commit(sqlite3.IntegrityError)
    mockdb.add_rollback()
    with pytest.raises(Duplicate) as e:
        db.create(1, 'test', 1, 0xABCDEF)

    assert type(e.value.__cause__) == sqlite3.IntegrityError


def test_delete(mockdb):
    mockdb.add_execute('DELETE FROM guest_media WHERE id = ?', ('test',), rowcount=1)
    mockdb.add_commit()
    assert db.delete('test') == 1


def test_update(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       UPDATE guest_media
                                       SET
                                       guest_id = ?,
                                       media_id = ?,
                                       sound = ?,
                                       color = ?
                                       WHERE id = ?
                                       ''').replace('\n', ' '), (1, 'test', 1, 0xABCDEF, 1), rowcount=1)
    mockdb.add_commit()
    assert db.update(1, 1, 'test', 1, 0xABCDEF) == 1


def test_update_NotFoundError(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       UPDATE guest_media
                                       SET
                                       guest_id = ?,
                                       media_id = ?,
                                       sound = ?,
                                       color = ?
                                       WHERE id = ?
                                       ''').replace('\n', ' '), (1, 'test', 1, 0xABCDEF, 1), rowcount=0)
    mockdb.add_commit()
    with pytest.raises(NotFound):
        db.update(1, 1, 'test', 1, 0xABCDEF)
