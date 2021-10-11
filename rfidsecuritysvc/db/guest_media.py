import sqlite3
import textwrap

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute(textwrap.dedent('''
                                            SELECT
                                            guest_media.id,
                                            guest_id,
                                            guest.first_name as guest_first_name,
                                            guest.last_name as guest_last_name,
                                            guest.default_sound as guest_default_sound,
                                            gs.name as guest_default_sound_name,
                                            guest.default_color as guest_default_color,
                                            media_id,
                                            media.name as media_name,
                                            media.desc as media_desc,
                                            guest_media.sound as sound_id,
                                            gms.name as sound_name,
                                            color
                                            FROM
                                            guest_media
                                            INNER JOIN media ON media.id = guest_media.media_id
                                            INNER JOIN guest ON guest.id = guest_media.guest_id
                                            LEFT JOIN sound gms ON gms.id = guest_media.sound
                                            LEFT JOIN sound gs ON gs.id = guest.default_sound
                                            WHERE guest_media.id = ?
                                            ORDER BY guest_media.id
                                            ''').replace('\n', ' '), (id,)).fetchone()


@with_dbconn
def get_by_media(conn, media_id):
    with conn:
        return conn.execute(textwrap.dedent('''
                                            SELECT
                                            guest_media.id,
                                            guest_id,
                                            guest.first_name as guest_first_name,
                                            guest.last_name as guest_last_name,
                                            guest.default_sound as guest_default_sound,
                                            gs.name as guest_default_sound_name,
                                            guest.default_color as guest_default_color,
                                            media_id,
                                            media.name as media_name,
                                            media.desc as media_desc,
                                            guest_media.sound as sound_id,
                                            gms.name as sound_name,
                                            color
                                            FROM
                                            guest_media
                                            INNER JOIN media ON media.id = guest_media.media_id
                                            INNER JOIN guest ON guest.id = guest_media.guest_id
                                            LEFT JOIN sound gms ON gms.id = guest_media.sound
                                            LEFT JOIN sound gs ON gs.id = guest.default_sound
                                            WHERE guest_media.media_id = ?
                                            ORDER BY guest_media.id
                                            ''').replace('\n', ' '), (media_id,)).fetchone()


@with_dbconn
def list(conn, guest_id=None):
    with conn:
        if guest_id:
            return conn.execute(textwrap.dedent('''
                                                SELECT
                                                guest_media.id,
                                                guest_id,
                                                guest.first_name as guest_first_name,
                                                guest.last_name as guest_last_name,
                                                guest.default_sound as guest_default_sound,
                                                gs.name as guest_default_sound_name,
                                                guest.default_color as guest_default_color,
                                                media_id,
                                                media.name as media_name,
                                                media.desc as media_desc,
                                                guest_media.sound as sound_id,
                                                gms.name as sound_name,
                                                color
                                                FROM
                                                guest_media
                                                INNER JOIN media ON media.id = guest_media.media_id
                                                INNER JOIN guest ON guest.id = guest_media.guest_id
                                                LEFT JOIN sound gms ON gms.id = guest_media.sound
                                                LEFT JOIN sound gs ON gs.id = guest.default_sound
                                                WHERE guest_media.guest_id = ?
                                                ORDER BY guest_media.id
                                                ''').replace('\n', ' '), (guest_id,)).fetchall()
        else:
            return conn.execute(textwrap.dedent('''
                                                SELECT
                                                guest_media.id,
                                                guest_id,
                                                guest.first_name as guest_first_name,
                                                guest.last_name as guest_last_name,
                                                guest.default_sound as guest_default_sound,
                                                gs.name as guest_default_sound_name,
                                                guest.default_color as guest_default_color,
                                                media_id,
                                                media.name as media_name,
                                                media.desc as media_desc,
                                                guest_media.sound as sound_id,
                                                gms.name as sound_name,
                                                color
                                                FROM
                                                guest_media
                                                INNER JOIN media ON media.id = guest_media.media_id
                                                INNER JOIN guest ON guest.id = guest_media.guest_id
                                                LEFT JOIN sound gms ON gms.id = guest_media.sound
                                                LEFT JOIN sound gs ON gs.id = guest.default_sound
                                                ORDER BY guest_media.id
                                                ''').replace('\n', ' ')).fetchall()


@with_dbconn
def create(conn, guest_id, media_id, sound_id=None, color=None):
    try:
        with conn:
            conn.execute('INSERT INTO guest_media (guest_id, media_id, sound, color) VALUES (?,?,?,?)', (guest_id, media_id, sound_id, color))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateGuestMediaError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM guest_media WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, guest_id, media_id, sound_id=None, color=None):
    with conn:
        count = conn.execute(textwrap.dedent('''
                                             UPDATE guest_media
                                             SET
                                             guest_id = ?,
                                             media_id = ?,
                                             sound = ?,
                                             color = ?
                                             WHERE id = ?
                                             ''').replace('\n', ' '), (guest_id, media_id, sound_id, color, id)).rowcount
    if count == 0:
        raise exception.GuestMediaNotFoundError

    return count
