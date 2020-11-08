import sqlite3
from rfidsecuritysvc.db.dbms import get_db
import rfidsecuritysvc.exception as exception

def list():
    return get_db().execute('SELECT media_id, permission.name as perm_name from media_perm INNER JOIN permission ON permission.id = media_perm.perm_id').fetchall()
