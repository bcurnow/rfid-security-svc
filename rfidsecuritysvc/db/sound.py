import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, name):
    with conn:
        return conn.execute('SELECT * FROM sound WHERE name = ?', (name,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT id, name, last_update_timestamp FROM sound ORDER BY id').fetchall()


@with_dbconn
def create(conn, name, content):
    try:
        with conn as conn:
            conn.execute('INSERT INTO sound (name, content) VALUES (?,?)', (name, content))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateSoundError from e


@with_dbconn
def delete(conn, name):
    with conn:
        return conn.execute('DELETE FROM sound WHERE name = ?', (name,)).rowcount


@with_dbconn
def update(conn, id, name, content=None):
    with conn:
        if content is None:
            count = conn.execute('UPDATE sound SET name = ? WHERE id = ?', (name, id)).rowcount
        else:
            count = conn.execute('UPDATE sound SET name = ?, content = ? WHERE id = ?', (name, content, id)).rowcount
    if count == 0:
        raise exception.SoundNotFoundError

    return count
