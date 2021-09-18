import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute('SELECT * FROM sound WHERE id = ?', (id,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT id, name FROM sound ORDER BY id').fetchall()


@with_dbconn
def create(conn, name, content):
    try:
        with conn as conn:
            conn.execute('INSERT INTO sound (name, content) VALUES (?,?)', (name, content))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateSoundError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM sound WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, name):
    with conn:
        count = conn.execute('UPDATE sound SET name = ? WHERE id = ?', (name, id)).rowcount
    if count == 0:
        raise exception.SoundNotFoundError

    return count
