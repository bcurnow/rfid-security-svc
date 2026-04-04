from functools import wraps
from typing import Any, Callable
import sys
import os
import sqlite3
from pathlib import Path


# Global database connection (thread-safe by check_same_thread=False)
_db_connection: sqlite3.Connection | None = None


def get_database_path() -> str:
    """Get the database path from environment or use default."""
    return os.environ.get('DATABASE', '/rfid-db/rfidsecurity.sqlite')


def init_db() -> bool:
    """Initialize the database schema only."""
    global _db_connection

    db_path = get_database_path()
    db_dir = Path(db_path).parent

    # Ensure directory exists
    if db_dir and not db_dir.exists():
        db_dir.mkdir(parents=True, exist_ok=True)

    # Create connection if needed
    if _db_connection is None:
        _db_connection = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False,  # Allow usage from async contexts
        )
        _db_connection.row_factory = sqlite3.Row
        _db_connection.execute('PRAGMA foreign_keys = ON')

    # Check if schema exists
    schema_exists = _db_connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config'").fetchone()

    if not schema_exists:
        sys.stderr.write('RFIDSecuritySvc: Database schema not detected, creating...')
        # Load and execute schema
        schema_sql = (Path(__file__).parent / 'schema.sql').read_text()
        _db_connection.executescript(schema_sql)
        sys.stderr.write('done!\n')
        return True  # Indicate that initialization was performed
    return False  # Schema already exists, no initialization needed


def get_connection() -> sqlite3.Connection:
    """Get the database connection, initializing if necessary."""
    global _db_connection

    if _db_connection is None:
        init_db()

    return _db_connection


def close_db() -> None:
    """Close the database connection."""
    global _db_connection

    if _db_connection is not None:
        try:
            print('Optimizing database before closing connection...', file=sys.stderr)
            _db_connection.execute('PRAGMA optimize')
        finally:
            _db_connection.close()
            _db_connection = None


def with_dbconn(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator which injects a database connection."""

    @wraps(func)
    def with_dbconn_impl(*args: Any, **kwargs: Any) -> Any:
        conn = get_connection()
        return func(conn, *args, **kwargs)

    return with_dbconn_impl
