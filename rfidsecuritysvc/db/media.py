import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
from rfidsecuritysvc import exception as exception


@with_dbconn
def get(conn: sqlite3.Connection, id: str) -> sqlite3.Row:
    with conn:
        return conn.execute('SELECT * FROM media WHERE id = ?', (id,)).fetchone()


@with_dbconn
def list(conn: sqlite3.Connection, exclude_associated: bool =  False) -> list[sqlite3.Row]:
    with conn:
        if exclude_associated:
            return conn.execute('SELECT media.* FROM media LEFT JOIN guest_media ON guest_media.media_id = media.id where guest_media.media_id IS NULL ORDER BY media.id').fetchall()
        return conn.execute('SELECT * FROM media ORDER BY id').fetchall()


@with_dbconn
def create(conn: sqlite3.Connection, id: str, name: str, desc: str = None) -> str:
    try:
        # Always make sure the ID is in upper case
        id = id.upper()
        with conn:
            conn.execute('INSERT INTO media (id, name, desc) VALUES (?,?,?)', (id, name, desc))
        return id
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateMediaError from e


@with_dbconn
def delete(conn: sqlite3.Connection, id: str) -> int:
    with conn:
        return conn.execute('DELETE FROM media WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn: sqlite3.Connection, id: str, name: str, desc: str) -> int:
    with conn:
        count = conn.execute('UPDATE media SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount
    if count == 0:
        raise exception.MediaNotFoundError

    return count
