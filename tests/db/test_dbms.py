import sqlite3
import pytest

from unittest.mock import Mock, patch

from flask import g

from rfidsecuritysvc.db.dbms import get_connection, close_db, init_db


@patch('rfidsecuritysvc.db.dbms.sqlite3')
def test_get_connection(sqlite3, app):
    with app.app_context():
        connection = Mock()
        sqlite3.connect.return_value = connection
        connection.execute.return_value = None
        get_connection()
        sqlite3.connect.assert_called_once_with(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        assert connection.row_factory == sqlite3.Row
        connection.execute.assert_called_once_with('PRAGMA foreign_keys = ON')


@patch('rfidsecuritysvc.db.dbms.sqlite3')
def test_connection_creates_single_connection(sqlite3, app):
    with app.app_context():
        assert get_connection() == get_connection()


def test_close_db(app):
    with app.app_context():
        db = get_connection()
        db.execute('SELECT 1')
        close_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        # If the connection is closed, this will generate an error
        db.execute('SELECT 1')
        assert 'Cannot operate on a closed database' in str(e.value)


def test_close_db_clears_g(app):
    with app.app_context():
        get_connection()
        assert 'db' in g
        theg = g.__dict__

    assert 'db' not in theg


def test_init_db(app):
    with app.app_context():
        table_names = ['config', 'media', 'media_perm', 'permission']
        connection = get_connection()

        # Start by making sure all the tables exist
        results = connection.execute('SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ?', ('table', 'sqlite_%')).fetchall()
        assert len(results) == len(table_names)
        for row in results:
            assert row['name'] in table_names

        # Now turn off foreign keys and drop the tables
        connection.execute('PRAGMA foreign_keys = OFF')
        for table in table_names:
            connection.execute(f'DROP TABLE {table}')

        # Verify the tables are gone
        results = connection.execute('SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ?', ('table', 'sqlite_%')).fetchall()
        assert len(results) == 0

        # Re-init the database
        init_db()

        # Validate that the tables have been re-created
        results = connection.execute('SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ?', ('table', 'sqlite_%')).fetchall()
        assert len(results) == len(table_names)
        for row in results:
            assert row['name'] in table_names
