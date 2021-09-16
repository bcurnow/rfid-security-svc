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

def test_by_media(mockdb):
    media_id = '12345'
    mockdb.add_execute(textwrap.dedent('''
                                       SELECT
                                       media_id,
                                       permission.name as perm_name
                                       FROM
                                       media_perm
                                       INNER JOIN permission ON permission.id = media_perm.perm_id
                                       WHERE media_id = ?
                                       ORDER BY media_perm.id
                                       ''').replace('\n', ' '), (media_id,), cursor_return=[])
    assert db.by_media(media_id) == []
