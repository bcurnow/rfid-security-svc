import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn: sqlite3.Connection, id: int) -> sqlite3.Row:
    with conn:
        return conn.execute('SELECT * FROM permission WHERE id = ?', (id,)).fetchone()


@with_dbconn
def get_by_name(conn: sqlite3.Connection, name: str) -> sqlite3.Row:
    with conn:
        return conn.execute('SELECT * FROM permission WHERE name = ?', (name,)).fetchone()


@with_dbconn
def list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    with conn:
        return conn.execute('SELECT * FROM permission ORDER BY id').fetchall()


@with_dbconn
def create(conn: sqlite3.Connection, name: str, desc: str) -> int:
    try:
        with conn:
            return conn.execute('INSERT INTO permission (name, desc) VALUES (?,?) RETURNING id', (name, desc)).fetchone()[0]
    except sqlite3.IntegrityError as e:
        raise exception.DuplicatePermissionError from e


@with_dbconn
def delete(conn: sqlite3.Connection, id: int) -> int:
    with conn:
        return conn.execute('DELETE FROM permission WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn: sqlite3.Connection, id: int, name: int, desc: int) -> int:
    with conn:
        count = conn.execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount
    if count == 0:
        raise exception.PermissionNotFoundError

    return count
