from rfidsecuritysvc.db.dbms import close_db


def test_teardown_appcontext(app):
    # Make sure the close_db function is registered
    assert close_db in app.teardown_appcontext_funcs
