from functools import wraps

import sqlite3
from flask import current_app, g


def get_connection():
    if 'db_connection' not in g:
        g.db_connection = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db_connection.row_factory = sqlite3.Row
        # Ensure that foreign_keys are turned on: https://www.sqlite.org/pragma.html#pragma_foreign_keys
        g.db_connection.execute('PRAGMA foreign_keys = ON')

    return g.db_connection


def close_db(e=None):
    connection = g.pop('db_connection', None)
    if connection is not None:
        # Optimize the database before we close it per https://www.sqlite.org/pragma.html#pragma_optimize
        try:
            connection.execute('PRAGMA optimize')
        finally:
            connection.close()


def with_dbconn(func):
    """Decorator which injects a database connection."""
    @wraps(func)
    def with_dbconn_impl(*args, **kwargs):
        conn = get_connection()
        return func(conn, *args, **kwargs)

    return with_dbconn_impl


def init_db():
    with current_app.open_resource('db/schema.sql') as f:
        get_connection().executescript(f.read().decode('utf8'))
