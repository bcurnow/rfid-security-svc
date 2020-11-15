import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, key):
    with conn:
        return conn.execute('SELECT * FROM config WHERE key = ?', (key,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT * FROM config ORDER BY key').fetchall()


@with_dbconn
def create(conn, key, value):
    try:
        with conn as conn:
            conn.execute('INSERT INTO config (key, value) VALUES (?,?)', (key, value))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateConfigError from e


@with_dbconn
def delete(conn, key):
    with conn:
        return conn.execute('DELETE FROM config WHERE key = ?', (key,)).rowcount


@with_dbconn
def update(conn, key, value):
    with conn:
        count = conn.execute('UPDATE config SET value = ? WHERE key = ?', (value, key)).rowcount
    if count == 0:
        raise exception.ConfigNotFoundError

    return count
