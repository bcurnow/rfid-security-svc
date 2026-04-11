import os
from contextlib import asynccontextmanager
from pathlib import Path
from connexion import AsyncApp
from connexion.resolver import RestyResolver
from connexion.options import SwaggerUIOptions
from rfidsecuritysvc.db.dbms import init_db, close_db
from rfidsecuritysvc.model.authorized import ensure_api_key


@asynccontextmanager
async def lifespan(app: AsyncApp):
    """Handle application startup and shutdown events."""
    # Startup
    if init_db():
        ensure_api_key()
    yield
    close_db()


def create_app(test_config=None):
    """Create and configure the Connexion application."""

    if test_config is not None:
        if 'DATABASE' in test_config:
            os.environ['DATABASE'] = test_config['DATABASE']
        if 'TESTING' in test_config:
            os.environ['TESTING'] = str(test_config['TESTING'])

    connexion_app = AsyncApp(
        __name__,
        specification_dir=str(Path(__file__).parent / 'api'),
        lifespan=lifespan,
        swagger_ui_options=SwaggerUIOptions(
            swagger_ui_config={
                'docExpansion': 'none',
                'persistAuthorization': True,
                'displayRequestDuration': True,
                'filter': True,
                'showCommonExtensions': True,
                'tryItOutEnabled': True,
            }
        ),
    )
    connexion_app.add_api('api.yaml', strict_validation=True, validate_responses=True, resolver=RestyResolver('rfidsecuritysvc.api'))

    return connexion_app


app = create_app()
