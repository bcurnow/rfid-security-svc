import os

from unittest.mock import Mock, patch

from rfidsecuritysvc.db.dbms import get_connection, close_db, init_db


@patch('rfidsecuritysvc.db.dbms.sqlite3')
def test_get_connection(sqlite3, app):
    from rfidsecuritysvc.db.dbms import close_db

    connection = Mock()
    cursor = Mock()
    cursor.fetchone.return_value = None

    def execute(sql, *args, **kwargs):
        if sql.startswith('PRAGMA foreign_keys'):
            return None
        if 'sqlite_master' in sql:
            return cursor
        return None

    connection.execute.side_effect = execute
    sqlite3.connect.return_value = connection

    close_db()

    get_connection()

    sqlite3.connect.assert_called_once_with(
        os.environ.get('DATABASE', '/rfid-db/rfidsecurity.sqlite'),
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False,
    )
    assert connection.row_factory == sqlite3.Row
    connection.execute.assert_any_call('PRAGMA foreign_keys = ON')


@patch('rfidsecuritysvc.db.dbms.sqlite3')
def test_connection_creates_single_connection(sqlite3, app):
    connection = Mock()
    sqlite3.connect.return_value = connection
    connection.execute.return_value = None

    conn1 = get_connection()
    conn2 = get_connection()
    assert conn1 is conn2


def test_close_db(app):
    db = get_connection()
    db.execute('SELECT 1')
    close_db()

    # After close_db, calling get_connection should return a new connection object
    new_db = get_connection()
    assert new_db is not db


def test_init_db(app):
    table_names = ['config', 'guest', 'guest_media', 'media', 'media_perm', 'permission', 'sound']
    connection = get_connection()

    results = connection.execute(
        'SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ?',
        ('table', 'sqlite_%'),
    ).fetchall()
    assert len(results) == len(table_names)
    for row in results:
        assert row['name'] in table_names

    connection.execute('PRAGMA foreign_keys = OFF')
    for table in table_names:
        connection.execute(f'DROP TABLE {table}')

    results = connection.execute(
        'SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ?',
        ('table', 'sqlite_%'),
    ).fetchall()
    assert len(results) == 0

    init_db()

    results = connection.execute(
        'SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE ?',
        ('table', 'sqlite_%'),
    ).fetchall()
    assert len(results) == len(table_names)
    for row in results:
        assert row['name'] in table_names
