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
                                            guest.id,
                                            guest.first_name,
                                            guest.last_name,
                                            guest.sound,
                                            sound.name as sound_name,
                                            sound.last_update_timestamp as sound_last_update_timestamp,
                                            guest.color
                                            FROM
                                            guest
                                            LEFT JOIN sound on guest.sound = sound.id
                                            WHERE guest.id = ?
                                            ORDER BY guest.id
                                            """).replace('\n', ' '),
            (id,),
        ).fetchone()


@with_dbconn
def list(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    with conn:
        return conn.execute(
            textwrap.dedent("""
                                            SELECT
                                            guest.id,
                                            guest.first_name,
                                            guest.last_name,
                                            guest.sound,
                                            sound.name as sound_name,
                                            sound.last_update_timestamp as sound_last_update_timestamp,
                                            guest.color
                                            FROM
                                            guest
                                            LEFT JOIN sound on guest.sound = sound.id
                                            ORDER BY guest.id
                                            """).replace('\n', ' ')
        ).fetchall()


@with_dbconn
def create(conn: sqlite3.Connection, first_name: str, last_name: str, sound: int = None, color: int = None) -> int:
    try:
        with conn as conn:
            return conn.execute(
                textwrap.dedent("""
                                         INSERT INTO guest
                                         (first_name, last_name, sound, color)
                                         VALUES (?,?,?,?)
                                         RETURNING id
                                         """).replace('\n', ' '),
                (first_name, last_name, sound, color),
            ).fetchone()[0]

    except sqlite3.IntegrityError as e:
        raise exception.DuplicateGuestError from e


@with_dbconn
def delete(conn: sqlite3.Connection, id: int) -> int:
    with conn:
        return conn.execute('DELETE FROM guest WHERE id = ?', (id,)).rowcount


@with_dbconn
def update(conn: sqlite3.Connection, id: int, first_name: str, last_name: str, sound: int = None, color: int = None) -> int:
    with conn:
        count = conn.execute(
            textwrap.dedent("""
                                             UPDATE guest
                                             SET first_name = ?, last_name = ?, sound = ?, color = ?
                                             WHERE id = ?
                                             """).replace('\n', ' '),
            (first_name, last_name, sound, color, id),
        ).rowcount
    if count == 0:
        raise exception.GuestNotFoundError

    return count
