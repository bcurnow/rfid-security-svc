import textwrap

from rfidsecuritysvc.db import association as db


def test_list(mockdb):
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       media_id,
                                       permission.name as perm_name
                                       FROM
                                       media_perm
                                       INNER JOIN permission ON permission.id = media_perm.perm_id
                                       ORDER BY media_perm.id
                                       ''').replace('\n', ' '), cursor_return=[])
    assert db.list() == []
