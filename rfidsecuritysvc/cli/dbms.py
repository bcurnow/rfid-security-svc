import click
from flask.cli import with_appcontext, AppGroup
from rfidsecuritysvc.db import dbms

group = AppGroup('db')


def register(app):
    app.cli.add_command(group)


@group.command('init')
@click.confirmation_option(prompt='Are you sure, this will delete all current data?')
@with_appcontext
def init_db():
    """Clear the existing data and create new tables."""
    dbms.init_db()
    click.echo(click.style('Initialized the database.', bg='green', fg='black'))
