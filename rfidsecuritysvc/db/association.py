import textwrap

from rfidsecuritysvc.db.dbms import with_dbconn


@with_dbconn
def list(conn):
    with conn:
        return conn.execute(textwrap.dedent('''
                                            SELECT
                                            media_id,
                                            permission.name as perm_name
                                            FROM
                                            media_perm
                                            INNER JOIN permission ON permission.id = media_perm.perm_id
                                            ORDER BY media_perm.id
                                            ''').replace('\n', ' ')).fetchall()

@with_dbconn
def by_media(conn, media_id):
    with conn:
        return conn.execute(textwrap.dedent('''
                                            SELECT
                                            media_id,
                                            permission.name as perm_name
                                            FROM
                                            media_perm
                                            INNER JOIN permission ON permission.id = media_perm.perm_id
                                            WHERE media_id = ?
                                            ORDER BY media_perm.id
                                            ''').replace('\n', ' '), (media_id,)).fetchall()
