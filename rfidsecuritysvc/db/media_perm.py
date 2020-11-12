import sqlite3
from rfidsecuritysvc.db.dbms import get_db
import rfidsecuritysvc.exception as exception


def get(id):
    return get_db().execute('SELECT * FROM media_perm WHERE id = ?', (id,)).fetchone()


def get_by_media_and_perm(media_id, perm_id):
    return get_db().execute('SELECT * FROM media_perm WHERE media_id = ? AND perm_id = ?', (media_id, perm_id)).fetchone()


def list():
    return get_db().execute('SELECT * FROM media_perm ORDER BY id').fetchall()


def create(media_id, perm_id):
    try:
        db = get_db()
        db.execute('INSERT INTO media_perm (media_id, perm_id) VALUES (?,?)', (media_id, perm_id))
        db.commit()
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateMediaPermError from e


def delete(id):
    db = get_db()
    count = db.execute('DELETE FROM media_perm WHERE id = ?', (id,)).rowcount
    db.commit()
    return count


def delete_by_media_and_perm(media_id, perm_id):
    db = get_db()
    count = db.execute('DELETE FROM media_perm WHERE media_id = ? AND perm_id = ?', (media_id, perm_id)).rowcount
    db.commit()
    return count


def update(id, media_id, perm_id):
    db = get_db()
    count = db.execute('UPDATE media_perm SET media_id = ?, perm_id = ? WHERE id = ?', (media_id, perm_id, id)).rowcount
    if count == 0:
        raise exception.MediaPermNotFoundError

    db.commit()
    return count
