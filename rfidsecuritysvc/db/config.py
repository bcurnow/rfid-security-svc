import sqlite3
from rfidsecuritysvc.db.dbms import get_db
import rfidsecuritysvc.exception as exception

def get(key):
    return get_db().execute('SELECT * FROM config WHERE key = ?', (key,)).fetchone()

def list():
    return get_db().execute('SELECT * FROM config ORDER BY key').fetchall()

def create(key, value):
    try:
        db = get_db()
        db.execute('INSERT INTO config (key, value) VALUES (?,?)', (key, value))
        db.commit()
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateConfigError from e

def delete(key):
    db = get_db()
    count = db.execute('DELETE FROM config WHERE key = ?', (key,)).rowcount
    db.commit()
    return count

def update(key, value):
    db = get_db()
    count =  db.execute('UPDATE config SET value = ? WHERE key = ?', (value, key)).rowcount
    if count == 0:
        raise exception.ConfigNotFoundError
    
    db.commit();
    return count
