import sqlite3
from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn, id):
    with conn:
        return conn.execute('SELECT * FROM media_perm WHERE id = ?', (id,)).fetchone()


@with_dbconn
def get_by_media_and_perm(conn, media_id, perm_id):
    with conn:
        return conn.execute('SELECT * FROM media_perm WHERE media_id = ? AND perm_id = ?', (media_id, perm_id)).fetchone()


@with_dbconn
def list(conn):
    with conn:
        return conn.execute('SELECT * FROM media_perm ORDER BY id').fetchall()


@with_dbconn
def create(conn, media_id, perm_id):
    try:
        with conn:
            conn.execute('INSERT INTO media_perm (media_id, perm_id) VALUES (?,?)', (media_id, perm_id))
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateMediaPermError from e


@with_dbconn
def delete(conn, id):
    with conn:
        return conn.execute('DELETE FROM media_perm WHERE id = ?', (id,)).rowcount


@with_dbconn
def delete_by_media_and_perm(conn, media_id, perm_id):
    with conn:
        return conn.execute('DELETE FROM media_perm WHERE media_id = ? AND perm_id = ?', (media_id, perm_id)).rowcount


@with_dbconn
def update(conn, id, media_id, perm_id):
    with conn:
        count = conn.execute('UPDATE media_perm SET media_id = ?, perm_id = ? WHERE id = ?', (media_id, perm_id, id)).rowcount
    if count == 0:
        raise exception.MediaPermNotFoundError

    return count
