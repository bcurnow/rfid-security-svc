import sqlite3
import textwrap

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception

SELECT_BASE = textwrap.dedent('''
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
                              guest_media.sound as sound,
                              gms.name as sound_name,
                              gms.last_update_timestamp as sound_last_update_timestamp,
                              guest_media.color
                              FROM
                              guest_media
                              INNER JOIN media ON media.id = guest_media.media_id
                              INNER JOIN guest ON guest.id = guest_media.guest_id
                              LEFT JOIN sound gms ON gms.id = guest_media.sound
                              LEFT JOIN sound gs ON gs.id = guest.sound
                              ''').replace('\n', ' ').strip()


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute(f'{SELECT_BASE} WHERE guest_media.id = ? ORDER BY guest_media.id', (id,)).fetchone()


@with_dbconn
def get_by_media(conn, media_id):
    with conn:
        return conn.execute(f'{SELECT_BASE} WHERE guest_media.media_id = ? ORDER BY guest_media.id', (media_id,)).fetchone()


@with_dbconn
def list(conn, guest_id=None):
    with conn:
        if guest_id:
            return conn.execute(f'{SELECT_BASE} WHERE guest_media.guest_id = ? ORDER BY guest_media.id', (guest_id,)).fetchall()
        else:
            return conn.execute(f'{SELECT_BASE} ORDER BY guest_media.id').fetchall()


@with_dbconn
def create(conn, guest_id, media_id, sound=None, color=None):
    try:
        with conn:
            conn.execute('INSERT INTO guest_media (guest_id, media_id, sound, color) VALUES (?,?,?,?)', (guest_id, media_id, sound, color))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateGuestMediaError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM guest_media WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, guest_id, media_id, sound=None, color=None):
    with conn:
        count = conn.execute(textwrap.dedent('''
                                             UPDATE guest_media
                                             SET
                                             guest_id = ?,
                                             media_id = ?,
                                             sound = ?,
                                             color = ?
                                             WHERE id = ?
                                             ''').replace('\n', ' '), (guest_id, media_id, sound, color, id)).rowcount
    if count == 0:
        raise exception.GuestMediaNotFoundError

    return count
