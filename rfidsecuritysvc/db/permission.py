import sqlite3
from rfidsecuritysvc.db.dbms import get_db
import rfidsecuritysvc.exception as exception

def get(id):
    return get_db().execute('SELECT * FROM permission WHERE id = ?', (id,)).fetchone()

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

def update(id, name, desc):
    db = get_db()
    if db.execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount == 0:
        raise exception.PermissionNotFoundError
    db.commit();
