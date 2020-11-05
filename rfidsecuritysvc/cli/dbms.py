import click
from flask.cli import with_appcontext, AppGroup
from rfidsecuritysvc.db import dbms

group = AppGroup('db')

def register(app)
  parent.add_command(group)

@db.command('init')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  click.confirm('Are you sure, this will delete all current data?', abort=True)
  dbms.init_db()
  click.echo('Initialized the database.')
