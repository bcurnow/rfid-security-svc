import os
import tempfile
import pytest
from types import ModuleType

import click
from unittest.mock import Mock, PropertyMock

from rfidsecuritysvc import create_app
from rfidsecuritysvc.db.dbms import get_db, init_db, close_db

# Read in a file with the test data we'll need
with open(os.path.join(os.path.dirname(__file__), 'db/data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """A Flask app class"""
    # Create a temporary director for this set of tests
    db_fd, db_path = tempfile.mkstemp()

    # Create an application with a testing indicator and override the default database path to our temp path
    app = create_app({
        'TESTING': True,
        'ENV': 'development',
        'DATABASE': db_path,
    })

    # Initialize a new database and load it with the test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    # allow the tests to run
    yield app

    # Close down the database properly
    with app.app_context():
        close_db()

    # Close and delete the temp directory
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class MockDb(object):
    def __init__(self):
        # Create a mock for the overall database
        self._db = Mock()
        # Ensure that the execute method calls this function to determine the return_value/side_effect
        self._db.execute.side_effect = self.get_return_value_for_execute
        # Need a global index to see which execute we're on
        self._db_execute_return_value_index = 0
        # Create a dict to store each execute call
        self._executes = {}

    def get_return_value_for_execute(self, *args, **kwargs):
        # If we get a call and we're out of return values, just return a Mock, this will return a better error message because we'll get to assert
        if self._db_execute_return_value_index > (len(self._executes[args[0]]) - 1):
            return Mock()

        # The first arg is the SQL statement, use it to get the executes array and use the global pointer to pull back the cursor for this execute
        rv = self._executes[args[0]][self._db_execute_return_value_index]['cursor']
        # Increment the index so next call returns the next value
        self._db_execute_return_value_index += 1
        return rv

    def get_db(self):
        return self._db

    def add_execute(self, sql, sql_args=None, cursor_return=None, rowcount=None):
        index = 0
        if sql in self._executes:
            index = len(self._executes) - 1
        else:
            # We don't yet have any registered executes for this SQL, create an empty list
            self._executes[sql] = []

        # Add a dict for this specific execute of the SQL
        self._executes[sql].append({})
        execute = self._executes[sql][index]
        execute['sql_args'] = sql_args
        self._add_cursor(execute, cursor_return, rowcount)

    def add_commit(self, side_effect=None):
        self._db.commit.side_effect = side_effect

    def assert_db(self):
        if len(self._executes) == 0:
            self._db.execute.assert_not_called()

        total_execs = 0
        for (sql, execs) in self._executes.items():
            for e in execs:
                total_execs += 1
                if e['sql_args']:
                    self._db.execute.assert_any_call(sql, e['sql_args'])
                else:
                    self._db.execute.assert_any_call(sql)
                    if 'cursor_return' in e:
                        e['cursor_return_method'].assert_called_once()
                        if 'rowcount' in e:
                            e['rowcount_mock'].assert_called_once()

        assert self._db.execute.call_count == total_execs

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

    # Find all the get_db methods and monekypatch them to return MockDb instead
    for name, val in request.module.__dict__.items():
        if isinstance(val, ModuleType):
            if 'rfidsecuritysvc.db' in val.__name__:
                get_db = getattr(val, 'get_db', None)
                if get_db:
                    monkeypatch.setattr(val, 'get_db', db.get_db, raising=True)

    yield db

    db.assert_db()


@pytest.fixture
def assert_output():
    def assert_output(result, msg, exit_code=0, **style):
        assert result.exit_code == exit_code
        if style:
            assert bytes(click.style(str(msg), **style), 'UTF-8') in result.stdout_bytes
        else:
            assert str(msg) in result.output

    return assert_output
