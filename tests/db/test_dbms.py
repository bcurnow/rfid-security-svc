import sqlite3
import pytest

from unittest.mock import Mock, patch

from flask import g

from rfidsecuritysvc.db.dbms import get_db


@patch('rfidsecuritysvc.db.dbms.sqlite3')
def test_get_db(sqlite3, app):
    with app.app_context():
        connection = Mock()
        sqlite3.connect.return_value = connection
        connection.execute.return_value = None
        get_db()
        sqlite3.connect.assert_called_once_with(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        assert connection.row_factory == sqlite3.Row
        connection.execute.assert_called_once_with('PRAGMA foreign_keys = ON')


@patch('rfidsecuritysvc.db.dbms.sqlite3')
def test_get_db_creates_single_connection(sqlite3, app):
    with app.app_context():
        assert get_db() == get_db()


def test_close_db(app):
    with app.app_context():
        db = get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        # If the connection is closed, this will generate an error
        db.execute('SELECT 1')
        assert 'Cannot operate on a closed database' in str(e.value)


def test_close_db_clears_g(app):
    with app.app_context():
        get_db()
        theg = g.__dict__

    assert 'db' not in theg
