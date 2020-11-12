import atexit
import os
from pathlib import Path

from connexion.exceptions import OAuthProblem
from connexion.resolver import RestyResolver
from swagger_ui_bundle import swagger_ui_3_path

from rfidsecuritysvc import create_app
from rfidsecuritysvc.db.dbms import close_db
from rfidsecuritysvc.util.exception import render_unauthorized


def test_create_app(app):
    assert app.connexion.import_name == 'rfidsecuritysvc'
    assert app.connexion.specification_dir == Path(app.root_path) / Path('api/')
    _assert_connexion_options(app.connexion.options.as_dict())
    _assert_api(app.api_yaml)
    assert app.error_handler_spec[None][401][OAuthProblem] == render_unauthorized
    _assert_test_app_config(app)
    assert os.path.exists(app.instance_path) is True
    _assert_bootstrap(app)


def test_create_app_non_test():
    """Manuallly creates an app to validate certain settings that can't be validated when running under a test"""
    app = create_app()
    _assert_default_app_config(app)


def test_create_app_config_py():
    """Creates a temporary config.py and ensures that our from_py load works as expected"""
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rfidsecuritysvc', 'config.py'))
    # Make sure someone hasn't added a config.py file first, if one exists, we should fail
    assert not os.path.exists(config_file)

    # Make sure that we cleanup the file
    atexit.register(_cleanup_config_file, config_file)

    with open(config_file, 'w') as f:
        f.write('TEST_CREATE_APP_CONFIG_PY=True\n')

    app = create_app()

    assert app.config['TEST_CREATE_APP_CONFIG_PY'] is True

    # Even though we registered the atexit function, we should be good stewards and cleanup our files now
    _cleanup_config_file(config_file)


def _cleanup_config_file(config_file):
    if os.path.exists(config_file):
        os.remove(config_file)


def _assert_connexion_options(options):
    assert options['instance_relative_config'] is True
    assert options['swagger_path'] == swagger_ui_3_path
    _assert_swappger_ui_config(options['swagger_ui_config'])


def _assert_swappger_ui_config(config):
    assert config['docExpansion'] == 'none'
    assert config['persistAuthorization'] is True


def _assert_api(api):
    assert api.strict_validation is True
    assert api.validate_responses is True
    assert type(api.resolver) == RestyResolver
    assert api.resolver.default_module_name == 'rfidsecuritysvc.api'


def _assert_test_app_config(app):
    """Why test this? Because it's production code that makes it happen even if it only fires when testing"""
    assert app.config['TESTING'] is True
    assert 'rfidsecurity.sqlite' not in app.config['DATABASE']


def _assert_default_app_config(app):
    assert app.config['SECRET_KEY'] == 'dev'
    assert app.config['DATABASE'] == os.path.join(app.instance_path, 'rfidsecurity.sqlite')
    assert app.config['JSON_SORT_KEYS'] is False
    # We aren't explicitly setting this but, just to be safe...
    assert app.config['TESTING'] is False


def _assert_bootstrap(app):
    # The commands will only be present if the bootstrap code is called, so check for those
    expected = ['auth', 'config', 'db', 'media', 'media-perm', 'permission', 'test']
    for cmd in app.cli.list_commands(app.app_context()):
        assert cmd in expected

    # Make sure the close_db function is registered
    assert close_db in app.teardown_appcontext_funcs
