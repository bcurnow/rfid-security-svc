import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn: sqlite3.Connection, id: int) -> sqlite3.Row:
    with conn:
        return conn.execute('SELECT * FROM sound WHERE id = ?', (id,)).fetchone()


@with_dbconn
def get_by_name(conn: sqlite3.Connection, name: str) -> sqlite3.Row:
    with conn:
        return conn.execute('SELECT * FROM sound WHERE name = ?', (name,)).fetchone()


@with_dbconn
def list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    with conn:
        return conn.execute('SELECT id, name, last_update_timestamp FROM sound ORDER BY id').fetchall()


@with_dbconn
def create(conn: sqlite3.Connection, name: str, content: str) -> int:
    try:
        with conn as conn:
            return conn.execute('INSERT INTO sound (name, content) VALUES (?,?) RETURNING id', (name, content)).fetchone()[0]
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateSoundError from e


@with_dbconn
def delete(conn: sqlite3.Connection, id: int) -> int:
    with conn:
        return conn.execute('DELETE FROM sound WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn: sqlite3.Connection, id: int, name: str, content: str = None) -> int:
    with conn:
        if content is None:
            count = conn.execute('UPDATE sound SET name = ? WHERE id = ?', (name, id)).rowcount
        else:
            count = conn.execute('UPDATE sound SET name = ?, content = ? WHERE id = ?', (name, content, id)).rowcount
    if count == 0:
        raise exception.SoundNotFoundError

    return count
