import click
from flask.cli import AppGroup
from rfidsecuritysvc.model import media_perm as model, media, permission

group = AppGroup('media-perm')

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
  pprint(json.dumps(tuple(record)))

@group.command('list')
def list_command():
  """List all the records in the table."""
  print(*model.list(), sep = '\n')

@group.command('create')
@click.argument('media_id')
@click.argument('perm_id')
@click.pass_context
def create_command(ctx, media_id, perm_id):
  """Manually adds a record to the table."""
  if not media.get(media_id):
    ctx.fail(click.style('No media found with id "{0}".'.format(media_id), fg='red'))
  if not permission.get(perm_id):
    ctx.fail(click.style('No permission found with id "{0}".'.format(perm_id), fg='red'))
  model.create(media_id, perm_id)
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
@click.argument('media_id')
@click.argument('perm_id')
@click.pass_context
def update_command(ctx, id, media_id, perm_id):
  """Manually updates a record in the table."""
  click.echo(str(model.update(id, media_id, perm_id)) + ' record(s) updated')
  ctx.invoke(list_command)
