import os
import connexion
from connexion.exceptions import OAuthProblem
from connexion.resolver import RestyResolver
from swagger_ui_bundle import swagger_ui_3_path
from flask import Flask
from rfidsecuritysvc.util.exception import render_unauthorized

def create_app(test_config=None):

    swagger_ui_config = {
        'docExpansion': 'none',
        'persistAuthorization': True,
    }

    connexion_options = {
        'instance_relative_config': True,
        'swagger_path': swagger_ui_3_path,
        'swagger_ui_config': swagger_ui_config,
    }

    # Setup Flask using the Connexion wrapper
    api_app = connexion.App(__name__, specification_dir='api/', options=connexion_options)
    api_app.add_api('api.yaml', strict_validation=True, validate_responses=True, resolver=RestyResolver(f'{__package__}.api'))

    # Add a custom renderer for OAuthProblems so we set the correct headers and return meaningful messages
    api_app.add_error_handler(OAuthProblem, render_unauthorized)

    # Get the wrapped Flask class so we can configure Flask
    app = api_app.app

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'rfidsecurity.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Bootstrap rfidsecuritysvc
    from rfidsecuritysvc.bootstrap import main
    main.bootstrap(app)

    return app
