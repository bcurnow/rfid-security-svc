import pytest
import sqlite3

from flask import g

from rfidsecuritysvc.db.dbms import get_db

def test_teardown_appcontext_clears_g(app):
    with app.app_context():
        get_db()
        assert 'db' in g
        # Get a copy of the internal dict for g since we won't be able to use the 'g' object after the context closes
        theglobals = g.__dict__

    assert 'db' not in theglobals

def test_teardown_appcontext_closes_db(app):
    with app.app_context():
        db = get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        # If the connection is closed, this will generate an error
        db.execute('SELECT 1')
        assert 'Cannot operate on a closed database' in str(e.value)
