from rfidsecuritysvc.db.dbms import get_db


def list():
    return get_db().execute('''
                            SELECT
                            media_id,
                            permission.name as perm_name
                            FROM
                            media_perm
                            INNER JOIN permission ON permission.id = media_perm.perm_id
                            ORDER BY media_perm.id
                            ''').fetchall()
