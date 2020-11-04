import click
import json
from flask.cli import AppGroup
from pprint import pprint as pprint
from rfidsecuritysvc.db import config as table

group = AppGroup('config')

def register(app, parent):
  parent.add_command(group)
  
@group.command('get')
@click.argument('key')
@click.pass_context
def get_command(ctx, key):
  """Gets a single record from the table."""
  record = table.get(key)
  if not record:
    ctx.fail(click.style('No record found with key "{0}".'.format(key), fg='red'))
  pprint(json.dumps(tuple(record)))

@group.command('list')
def list_command():
  """List all the records in the table."""
  for m in table.list():
    pprint(json.dumps(tuple(m)))

@group.command('create')
@click.argument('key')
@click.argument('value')
@click.pass_context
def create_command(ctx, key, value):
  """Manually adds a record to the table."""
  table.create(key, value)
  ctx.invoke(list_command)

@group.command('delete')
@click.argument('key')
@click.pass_context
def delete_command(ctx, key):
  """Manually deletes a record from the table."""
  click.echo(str(table.delete(key)) + ' record(s) deleted')
  ctx.invoke(list_command)

@group.command('update')
@click.argument('key')
@click.argument('value', required=False)
@click.pass_context
def update_command(ctx, key, value):
  """Manually updates a record in the table."""
  click.echo(str(table.update(key, value)) + ' record(s) updated')
  ctx.invoke(list_command)
