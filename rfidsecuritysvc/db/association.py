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
