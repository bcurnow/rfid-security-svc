import sqlite3
import textwrap

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute('SELECT * FROM guest WHERE id = ?', (id,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT * FROM guest ORDER BY id').fetchall()


@with_dbconn
def create(conn, first_name, last_name, default_sound=None, default_color=None):
    try:
        with conn as conn:
            conn.execute(textwrap.dedent('''
                                         INSERT INTO guest
                                         (first_name, last_name, default_sound, default_color)
                                         VALUES (?,?,?,?)
                                         ''').replace('\n', ' '), (first_name, last_name, default_sound, default_color))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateGuestError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM guest WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, first_name, last_name, default_sound=None, default_color=None):
    with conn:
        count = conn.execute(textwrap.dedent('''
                                             UPDATE guest
                                             SET first_name = ?, last_name = ?, default_sound = ?, default_color = ?
                                             WHERE id = ?
                                             ''').replace('\n', ' '), (first_name, last_name, default_sound, default_color, id)).rowcount
    if count == 0:
        raise exception.GuestNotFoundError

    return count
