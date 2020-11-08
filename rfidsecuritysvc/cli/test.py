import click
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

import rfidsecuritysvc.exception as exception

group = AppGroup('test')

def register(app):
    app.cli.add_command(group)

@group.command('generate-test-apikey')
@click.argument('value')
def generate_api_key(value):
    """ Takes the value from the command line and generates a password_hash that can then be used to populate the
    rfidsecuritysvc.api.auth.ADMIN_API_KEY value in your test data and ensures a well known value for testing """
    click.echo(generate_password_hash(value))
