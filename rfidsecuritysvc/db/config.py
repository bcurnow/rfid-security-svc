import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn: sqlite3.Connection, key: str) -> sqlite3.Row:
    with conn:
        return conn.execute('SELECT * FROM config WHERE key = ?', (key,)).fetchone()


@with_dbconn
def list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    with conn:
        return conn.execute('SELECT * FROM config ORDER BY key').fetchall()


@with_dbconn
def create(conn: sqlite3.Connection, key: str, value: str) -> str:
    try:
        with conn as conn:
            conn.execute('INSERT INTO config (key, value) VALUES (?,?)', (key, value))
        return key
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateConfigError from e


@with_dbconn
def delete(conn: sqlite3.Connection, key: str) -> int:
    with conn:
        return conn.execute('DELETE FROM config WHERE key = ?', (key,)).rowcount


@with_dbconn
def update(conn: sqlite3.Connection, key: str, value: str) -> int:
    with conn:
        count = conn.execute('UPDATE config SET value = ? WHERE key = ?', (value, key)).rowcount
    if count == 0:
        raise exception.ConfigNotFoundError

    return count


@with_dbconn
def replace(conn: sqlite3.Connection, key: str, value: str) -> None:
    try:
        with conn:
            count = conn.execute('REPLACE INTO config (key, value) VALUES (?,?)', (key, value)).rowcount
        if count == 0:
            raise exception.ConfigNotFoundError
        
        return count
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateConfigError from e
