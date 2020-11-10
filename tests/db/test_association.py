import pytest
import sqlite3

from rfidsecuritysvc.db import association as db

def test_list(mockdb):
    mockdb.add_execute('SELECT media_id, permission.name as perm_name from media_perm INNER JOIN permission ON permission.id = media_perm.perm_id', cursor_return=[])
    assert db.list() == []
