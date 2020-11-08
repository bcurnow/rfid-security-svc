import sqlite3
import pytest

from flask import g, appcontext_popped, appcontext_pushed

from rfidsecuritysvc.db.dbms import get_db

def test_get_db_creates_single_connection(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

def test_get_db_enables_foreign_keys(app):
    with app.app_context():
        db = get_db()
        assert db.execute('PRAGMA foreign_keys').fetchone()['foreign_keys'] == 1

def test_get_db_configures_sqlite3_row(app):
    with app.app_context():
        db = get_db()
        assert db.row_factory == sqlite3.Row

def test_autoclose_closes_connection(app):
    with app.app_context():
        db = get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'Cannot operate on a closed database' in str(e.value)

