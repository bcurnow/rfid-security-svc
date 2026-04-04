import os

from connexion.options import SwaggerUIOptions
from rfidsecuritysvc import create_app


def test_create_app(app):
    app = create_app()
    assert app.middleware.options is not None
    options = app.middleware.options
    assert options.arguments is None
    assert options.auth_all_paths is None
    assert options.jsonifier is None
    assert options.pythonic_params is None
    assert options.resolver is None
    assert options.resolver_error is None
    assert options.resolver_error_handler is None
    assert options.strict_validation is None
    assert options.swagger_ui_options is not None
    assert options.swagger_ui_options == SwaggerUIOptions(
        serve_spec=True,
        swagger_ui=True,
        swagger_ui_config={
            'displayRequestDuration': True,
            'docExpansion': 'none',
            'filter': True,
            'persistAuthorization': True,
            'showCommonExtensions': True,
            'tryItOutEnabled': True,
        },
        swagger_ui_path='/ui',
        swagger_ui_template_dir=None,
        swagger_ui_template_arguments={},
    )
    assert options.uri_parser_class is None
    assert options.validate_responses is None
    assert options.validator_map is None
    assert options.security_map is None


def test_create_app_testing_database():
    create_app(test_config={'DATABASE': 'testvalue'})
    assert os.environ.get('DATABASE') == 'testvalue'


def test_create_app_testing_testing():
    create_app(test_config={'TESTING': True})
    assert os.environ.get('TESTING') == 'True'
