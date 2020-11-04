import click
from flask.cli import with_appcontext
from rfidsecuritysvc.db import dbms

def register(app, parent):
  parent.add_command(init_db_command)

@click.command('init')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  click.confirm('Are you sure, this will delete all current data?', abort=True)
  dbms.init_db()
  click.echo('Initialized the database.')
