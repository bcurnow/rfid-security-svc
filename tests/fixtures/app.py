import os
import pytest
import tempfile

from rfidsecuritysvc import create_app
from rfidsecuritysvc.db import config, guest, media, permission, media_perm, sound
from rfidsecuritysvc.db.dbms import init_db, close_db


@pytest.fixture(scope='session')
def app(configs, guests, medias, permissions, media_perms, sounds):
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
        for model, objects in {
            config: configs,
            guest: guests,
            media: medias,
            permission: permissions,
            media_perm: media_perms,
            sound: sounds,
        }.items():
            for o in objects:
                model.create(**o.to_json_rw())

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
