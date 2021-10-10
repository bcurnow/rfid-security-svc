import sqlite3

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute('SELECT * FROM permission WHERE id = ?', (id,)).fetchone()


@with_dbconn
def get_by_name(conn, name):
    with conn:
        return conn.execute('SELECT * FROM permission WHERE name = ?', (name,)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT * FROM permission ORDER BY id').fetchall()


@with_dbconn
def create(conn, name, desc):
    try:
        with conn:
            conn.execute('INSERT INTO permission (name, desc) VALUES (?,?)', (name, desc))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicatePermissionError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM permission WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn, id, name, desc):
    with conn:
        count = conn.execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount
    if count == 0:
        raise exception.PermissionNotFoundError

    return count
