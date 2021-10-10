import hashlib
import importlib
import pytest
from types import ModuleType
from unittest.mock import Mock, PropertyMock

from rfidsecuritysvc.db import dbms


class SQLStringNotFound(Exception):
    pass


class MockDb(object):
    def __init__(self):
        # Create a mock for the overall database connection
        self._conn = Mock()
        self._setup_conn()
        # Need a global index to see which execute we're on
        self._conn_execute_return_value_index = 0
        # Create a dict to store each execute call
        self._executes = {}
        # By default, no commit or rollback will be called
        self.commit = False
        self.rollback = False

    def _setup_conn(self):
        # Setup a local variable because we can't use self._conn within the class we define
        conn = self._conn

        # Ensure that the execute method calls this function to determine the return_value/side_effect
        conn.execute.side_effect = self.get_return_value_for_execute

        # Create a context manager implementation to ensure that commit and rollback get called
        class mock_context_manager():

            def __enter__(self):
                return conn

            def __exit__(self, type, value, traceback):
                # Trying to replicate the functionality of sqlite3 as closely as possible
                if type is None and value is None and traceback is None:
                    conn.commit()
                else:
                    conn.rollback()

        # We use the connection as a context manager so we need to mock out those methods
        conn.__enter__ = mock_context_manager.__enter__
        conn.__exit__ = mock_context_manager.__exit__

    def get_return_value_for_execute(self, *args, **kwargs):
        key = hashlib.sha256(bytes(args[0], 'utf-8')).hexdigest()
        if key not in self._executes:
            raise SQLStringNotFound(f'"{args[0]}"')

        # If we get a call and we're out of return values, just return a Mock, this will return a better error message because we'll get to assert
        if self._conn_execute_return_value_index > (len(self._executes[key]) - 1):
            return Mock()

        # The first arg is the SQL statement, use it to get the executes array and use the global pointer to pull back the cursor for this execute
        rv = self._executes[key][self._conn_execute_return_value_index]['cursor']
        # Increment the index so next call returns the next value
        self._conn_execute_return_value_index += 1
        return rv

    def with_dbconn(self, func):
        """This function replaces the with_dbconn decorator from rfidsecuritysvc.db.dbms with one that provides the MockDB"""
        def with_dbconn_impl(*args, **kwargs):
            return func(self._conn, *args, **kwargs)

        return with_dbconn_impl

    def add_execute(self, sql, sql_args=None, cursor_return=None, rowcount=None):
        index = 0
        key = hashlib.sha256(bytes(sql, 'utf-8')).hexdigest()

        if key in self._executes:
            index = len(self._executes) - 1
        else:
            # We don't yet have any registered executes for this SQL, create an empty list
            self._executes[key] = []

        # Add a dict for this specific execute of the SQL
        self._executes[key].append({})
        execute = self._executes[key][index]
        execute['sql'] = sql
        execute['sql_args'] = sql_args
        self._add_cursor(execute, cursor_return, rowcount)

    def add_commit(self, side_effect=None):
        self.commit = True
        self._conn.commit.side_effect = side_effect

    def add_rollback(self, side_effect=None):
        self.rollbackup = True
        self._conn.rollback.side_effect = side_effect

    def assert_db(self):
        if len(self._executes) == 0:
            self._conn.execute.assert_not_called()

        total_execs = 0
        for (key, execs) in self._executes.items():
            for e in execs:
                total_execs += 1
                if e['sql_args']:
                    self._conn.execute.assert_any_call(e['sql'], e['sql_args'])
                else:
                    self._conn.execute.assert_any_call(e['sql'])
                    if 'cursor_return' in e:
                        e['cursor_return_method'].assert_called_once()
                        if 'rowcount' in e:
                            e['rowcount_mock'].assert_called_once()

        assert self._conn.execute.call_count == total_execs

        if self.commit:
            self._conn.commit.assert_called_once()

        if self.rollback:
            self._conn.rollback.assert_called_once()

    def _add_cursor(self, execute, cursor_return, rowcount):
        """Creates a cursor mock and populates the return value"""
        cursor = Mock()
        execute['cursor'] = cursor

        if self._is_iterable(cursor_return):
            # Assume fetchall
            execute['cursor_return'] = cursor_return
            execute['cursor_return_method'] = cursor.fetchall
            cursor.fetchall.return_value = cursor_return
        elif cursor_return is None:
            # Assume this is a DELETE, UPDATE, INSERT, etc
            execute['cursor_return_method'] = None
        else:
            # Assume it is a single return (either a non-iterable value or None)
            execute['cursor_return'] = cursor_return
            execute['cursor_return_method'] = cursor.fetchone
            cursor.fetchone.return_value = cursor_return

        if rowcount is not None:
            execute['rowcount'] = rowcount
            p = PropertyMock(return_value=rowcount)
            execute['rowcount_mock'] = p
            type(cursor).rowcount = p

    def _is_iterable(self, arg):
        """
        Returns true if the passed in object has an __iter__ attribute but is neither a string nor an array of bytes
        (which are iterable but not in the way we mean)
        """
        return hasattr(arg, '__iter__') and not isinstance(arg, (str, bytes))


@pytest.fixture
def mockdb(request, monkeypatch):
    db = MockDb()

    # Save the original method
    orig_with_dbconn = dbms.with_dbconn

    # Replace the function only if we have a specific type of test
    dbms.with_dbconn = db.with_dbconn

    # Find all the imports from this test which come from rfidsecuritysvc.db so we can reload them
    db_mods = []
    for name, val in request.module.__dict__.items():
        if isinstance(val, ModuleType):
            if 'rfidsecuritysvc.db' in val.__name__:
                db_mods.append(val)

    # Reload all the rfidsecuritysvc.db modules we found to make the new mock with_dbconn take effect
    for mod in db_mods:
        importlib.reload(mod)

    # Run the test
    yield db

    # Put the original function back
    dbms.with_dbconn = orig_with_dbconn

    # Reload all the modules again
    for mod in db_mods:
        importlib.reload(mod)

    db.assert_db()
