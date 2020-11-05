import click
from flask.cli import AppGroup
from rfidsecuritysvc.model import permission as model

group = AppGroup('permission')

def register(app):
  app.cli.add_command(group)
  
@group.command('get')
@click.argument('id')
@click.pass_context
def get_command(ctx, id):
  """Gets a single record from the table."""
  record = model.get(id)
  if not record:
    ctx.fail(click.style('No record found with id "{0}".'.format(id), fg='red'))
    print(record.to_json())

@group.command('list')
def list_command():
  """List all the records in the table."""
  print(*model.list(), sep = "\n")

@group.command('create')
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def create_command(ctx, name, desc):
  """Manually adds a record to the table."""
  model.create(name, desc)
  ctx.invoke(list_command)

@group.command('delete')
@click.argument('id')
@click.pass_context
def delete_command(ctx, id):
  """Manually deletes a record from the table."""
  click.echo(str(model.delete(id)) + ' record(s) deleted')
  ctx.invoke(list_command)

@group.command('update')
@click.argument('id')
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def update_command(ctx, id, name, desc):
  """Manually updates a record in the table."""
  click.echo(str(model.update(id, name, desc)) + ' record(s) updated')
  ctx.invoke(list_command)
