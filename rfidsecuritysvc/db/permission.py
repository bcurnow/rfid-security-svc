import sqlite3
from rfidsecuritysvc.db.dbms import get_db
import rfidsecuritysvc.exception as exception

def get(id):
    return get_db().execute('SELECT * FROM permission WHERE id = ?', (id,)).fetchone()

def get_by_name(name):
    return get_db().execute('SELECT * FROM permission WHERE name = ?', (name,)).fetchone()

def list():
    return get_db().execute('SELECT * FROM permission ORDER BY id').fetchall()

def create(name, desc):
    try:
        db = get_db()
        db.execute('INSERT INTO permission (name, desc) VALUES (?,?)', (name, desc))
        db.commit()
    except sqlite3.IntegrityError as e:
        raise exception.DuplicatePermissionError from e

def delete(id):
    db = get_db()
    count = db.execute('DELETE FROM permission WHERE id = ?', (id,)).rowcount
    db.commit()
    return count

def delete_by_name(name):
    db = get_db()
    count = db.execute('DELETE FROM permission WHERE name = ?', (name,)).rowcount
    db.commit()
    return count

def update(id, name, desc):
    db = get_db()
    if db.execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount == 0:
        raise exception.PermissionNotFoundError
    db.commit();

def update_by_name(name, desc):
    db = get_db()
    count = db.execute('UPDATE permission SET desc = ? WHERE NAME = ?', (desc,name)).rowcount
    if count == 0:
        raise exception.PermissionNotFoundError

    db.commit()
    return count
