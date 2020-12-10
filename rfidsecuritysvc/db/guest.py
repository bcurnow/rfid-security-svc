import sqlite3

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
def create(conn, first_name, last_name):
    try:
        with conn as conn:
            conn.execute('INSERT INTO guest (first_name, last_name) VALUES (?,?)', (first_name, last_name))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateGuestError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM guest WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, first_name, last_name):
    with conn:
        count = conn.execute('UPDATE guest SET first_name = ?, last_name = ? WHERE id = ?', (first_name, last_name, id)).rowcount
    if count == 0:
        raise exception.GuestNotFoundError

    return count
