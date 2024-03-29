import sqlite3
import textwrap

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute(textwrap.dedent('''
                                            SELECT
                                            guest.id,
                                            guest.first_name,
                                            guest.last_name,
                                            guest.sound,
                                            sound.name as sound_name,
                                            sound.last_update_timestamp as sound_last_update_timestamp,
                                            guest.color
                                            FROM
                                            guest
                                            LEFT JOIN sound on guest.sound = sound.id
                                            WHERE guest.id = ?
                                            ORDER BY guest.id
                                            ''').replace('\n', ' '), (id,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute(textwrap.dedent('''
                                            SELECT
                                            guest.id,
                                            guest.first_name,
                                            guest.last_name,
                                            guest.sound,
                                            sound.name as sound_name,
                                            sound.last_update_timestamp as sound_last_update_timestamp,
                                            guest.color
                                            FROM
                                            guest
                                            LEFT JOIN sound on guest.sound = sound.id
                                            ORDER BY guest.id
                                            ''').replace('\n', ' ')).fetchall()


@with_dbconn
def create(conn, first_name, last_name, sound=None, color=None):
    try:
        with conn as conn:
            conn.execute(textwrap.dedent('''
                                         INSERT INTO guest
                                         (first_name, last_name, sound, color)
                                         VALUES (?,?,?,?)
                                         ''').replace('\n', ' '), (first_name, last_name, sound, color))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateGuestError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM guest WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, first_name, last_name, sound=None, color=None):
    with conn:
        count = conn.execute(textwrap.dedent('''
                                             UPDATE guest
                                             SET first_name = ?, last_name = ?, sound = ?, color = ?
                                             WHERE id = ?
                                             ''').replace('\n', ' '), (first_name, last_name, sound, color, id)).rowcount
    if count == 0:
        raise exception.GuestNotFoundError

    return count
