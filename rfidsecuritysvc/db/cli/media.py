import click
import json
from flask.cli import AppGroup
from pprint import pprint as pprint
from rfidsecuritysvc.db import media as table

group = AppGroup('media')

def register(app, parent):
  parent.add_command(group)
  
@group.command('get')
@click.argument('id')
@click.pass_context
def get_command(ctx, id):
  """Gets a single record from the table."""
  record = table.get(id)
  if not record:
    ctx.fail(click.style('No record found with id "{0}".'.format(id), fg='red'))
  pprint(json.dumps(tuple(record)))

@group.command('list')
def list_command():
  """List all the records in the table."""
  for m in table.list():
    pprint(json.dumps(tuple(m)))

@group.command('create')
@click.argument('id')
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def create_command(ctx, id, name, desc):
  """Manually adds a record to the table."""
  table.create(id, name, desc)
  ctx.invoke(list_command)

@group.command('delete')
@click.argument('id')
@click.pass_context
def delete_command(ctx, id):
  """Manually deletes a record from the table."""
  click.echo(str(table.delete(id)) + ' record(s) deleted')
  ctx.invoke(list_command)

@group.command('update')
@click.argument('id')
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def update_command(ctx, id, name, desc):
  """Manually updates a record in the table."""
  click.echo(str(table.update(id, name, desc)) + ' record(s) updated')
  ctx.invoke(list_command)
