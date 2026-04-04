import os
import pytest
import tempfile
from datetime import datetime, timezone

from starlette.testclient import TestClient

from rfidsecuritysvc import create_app
from rfidsecuritysvc.db import config, guest, guest_media, media, permission, media_perm, sound
from rfidsecuritysvc.db.dbms import close_db


@pytest.fixture(scope='session')
def app(configs, guests, guest_medias, medias, permissions, media_perms, sounds):
    """A Connexion test application"""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'ENV': 'development',
        'DATABASE': db_path,
    })

    for table, objects in {
        config: configs,
        guest: guests,
        guest_media: guest_medias,
        media: medias,
        permission: permissions,
        media_perm: media_perms,
        sound: sounds,
    }.items():
        for o in objects:
            table.create(**o.test_create())

    # Reset the last_update_timestamp for sounds to ensure they are in a consistent format for testing
    for s in sounds:
        db_sound = sound.get(s.id)
        t = datetime.fromisoformat(db_sound['last_update_timestamp'])
        t = t.replace(tzinfo=timezone.utc)
        s.last_update_timestamp = t.isoformat(timespec='seconds')

    yield app

    close_db()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='session')
def client(app):
    return TestClient(app)

