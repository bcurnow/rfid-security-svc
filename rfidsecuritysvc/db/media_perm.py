import sqlite3
import textwrap

from rfidsecuritysvc.db.dbms import with_dbconn
import rfidsecuritysvc.exception as exception


@with_dbconn
def get(conn: sqlite3.Connection, id: int) -> sqlite3.Row:
    with conn:
        return conn.execute(
            textwrap.dedent("""
                                            SELECT
                                            media_perm.id,
                                            media_id,
                                            media.name as media_name,
                                            media.desc as media_desc,
                                            permission_id,
                                            permission.name as permission_name,
                                            permission.desc as permission_desc
                                            FROM
                                            media_perm
                                            INNER JOIN media on media.id = media_perm.media_id
                                            INNER JOIN permission ON permission.id = media_perm.permission_id
                                            WHERE media_perm.id = ?
                                            ORDER BY media_perm.id
                                            """).replace('\n', ' '),
            (id,),
        ).fetchone()


@with_dbconn
def get_by_media_and_perm(conn: sqlite3.Connection, media_id: str, permission_name: str) -> sqlite3.Row:
    with conn:
        return conn.execute(
            textwrap.dedent("""
                                            SELECT
                                            media_perm.id,
                                            media_id,
                                            media.name as media_name,
                                            media.desc as media_desc,
                                            permission_id,
                                            permission.name as permission_name,
                                            permission.desc as permission_desc
                                            FROM
                                            media_perm
                                            INNER JOIN media on media.id = media_perm.media_id
                                            INNER JOIN permission ON permission.id = media_perm.permission_id
                                            WHERE media_perm.media_id = ? AND permission.name = ?
                                            ORDER BY media_perm.id
                                            """).replace('\n', ' '),
            (media_id, permission_name),
        ).fetchone()


@with_dbconn
def list(conn: sqlite3.Connection, media_id: str  = None) -> list[sqlite3.Row]:
    with conn:
        if media_id:
            return conn.execute(
                textwrap.dedent("""
                                                SELECT
                                                media_perm.id,
                                                media_id,
                                                media.name as media_name,
                                                media.desc as media_desc,
                                                permission_id,
                                                permission.name as permission_name,
                                                permission.desc as permission_desc
                                                FROM
                                                media_perm
                                                INNER JOIN media on media.id = media_perm.media_id
                                                INNER JOIN permission ON permission.id = media_perm.permission_id
                                                WHERE media_id = ?
                                                ORDER BY media_perm.id
                                                """).replace('\n', ' '),
                (media_id,),
            ).fetchall()
        else:
            return conn.execute(
                textwrap.dedent("""
                                                SELECT
                                                media_perm.id,
                                                media_id,
                                                media.name as media_name,
                                                media.desc as media_desc,
                                                permission_id,
                                                permission.name as permission_name,
                                                permission.desc as permission_desc
                                                FROM
                                                media_perm
                                                INNER JOIN media on media.id = media_perm.media_id
                                                INNER JOIN permission ON permission.id = media_perm.permission_id
                                                ORDER BY media_perm.id
                                                """).replace('\n', ' ')
            ).fetchall()


@with_dbconn
def create(conn: sqlite3.Connection, media_id: str, permission_id: int) -> int:
    try:
        with conn:
            return conn.execute('INSERT INTO media_perm (media_id, permission_id) VALUES (?,?) RETURNING id', (media_id, permission_id)).fetchone()[0]
    except sqlite3.IntegrityError as e:
        raise exception.DuplicateMediaPermError from e


@with_dbconn
def delete(conn: sqlite3.Connection, id: int) -> int:
    with conn:
        return conn.execute('DELETE FROM media_perm WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn: sqlite3.Connection, id: int, media_id: str, permission_id: int) -> int:
    with conn:
        count = conn.execute('UPDATE media_perm SET media_id = ?, permission_id = ? WHERE id = ?', (media_id, permission_id, id)).rowcount
    if count == 0:
        raise exception.MediaPermNotFoundError

    return count
