import sqlite3
from flask import current_app, g


def get_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def with_dbconn(func):
    """Decorator which injects a database connection."""
    def with_dbconn_impl(*args, **kwargs):
        conn = get_connection()
        return func(conn, *args, **kwargs)

    return with_dbconn_impl


def init_db():
    with current_app.open_resource('db/schema.sql') as f:
        get_connection().executescript(f.read().decode('utf8'))
