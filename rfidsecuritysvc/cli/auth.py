import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.api import auth

group = AppGroup('auth')

def register(app):
    app.cli.add_command(group)

@group.command('generate-api-key')
@click.pass_context
def generate_api_key(ctx):
    """Generates a new 512 bit secure token to be used to access the API, this will replace any current key"""
    click.confirm("Are you sure, this will invalidate the old key?", abort=True)
    key = auth.generate_api_key()
    click.echo(click.style(f'Generated new key "{key}", please record this value as it is not retrievable', bg='green', fg='black'))
