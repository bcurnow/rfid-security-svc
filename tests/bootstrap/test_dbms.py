from flask import g

from rfidsecuritysvc.db.dbms import get_db

def test_teardown_appcontext_clears_g(app):
    with app.app_context():
        get_db()
        assert 'db' in g
        # Get a copy of the internal dict for g since we won't be able to use the 'g' object after the context closes
        theglobals = g.__dict__

    assert 'db' not in theglobals
