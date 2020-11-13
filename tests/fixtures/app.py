import os
import pytest
import tempfile

from rfidsecuritysvc import create_app
from rfidsecuritysvc.db import config, media, permission, media_perm
from rfidsecuritysvc.db.dbms import init_db, close_db


@pytest.fixture(scope='session')
def app(configs, medias, permissions, media_perms):
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
        for c in configs:
            config.create(**c.to_json())

        for m in medias:
            media.create(**m.to_json())

        for p in permissions:
            permission.create(p.name, p.desc)

        for mp in media_perms:
            media_perm.create(mp.media_id, mp.perm_id)

    # allow the tests to run
    yield app

    # Close down the database properly
    with app.app_context():
        close_db()

    # Close and delete the temp directory
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()
