import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
from rfidsecuritysvc import exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute('SELECT * FROM media WHERE id = ?', (id,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT * FROM media ORDER BY id').fetchall()


@with_dbconn
def create(conn, id, name, desc=None):
    try:
        # Always make sure the ID is in upper case
        id = id.upper()
        with conn:
            conn.execute('INSERT INTO media (id, name, desc) VALUES (?,?,?)', (id, name, desc))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateMediaError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM media WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, name, desc):
    with conn:
        count = conn.execute('UPDATE media SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount
    if count == 0:
        raise exception.MediaNotFoundError

    return count
