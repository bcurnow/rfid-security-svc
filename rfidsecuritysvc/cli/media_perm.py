import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import media_perm as model, media, permission

group = AppGroup('media-perm')

def register(app):
    app.cli.add_command(group)

@group.command('get')
@click.argument('id')
@click.pass_context
def get(ctx, id):
    """Gets a single record from the table."""
    record = model.get(id)
    if not record:
        ctx.fail(click.style(f'No record found with id "{id}".', fg='red'))

    click.echo(record.to_json())

@group.command('list')
def list():
    """List all the records in the table."""
    for i in model.list():
        click.echo(i.to_json())

@group.command('create')
@click.argument('media_id')
@click.argument('perm_id')
@click.pass_context
def create(ctx, media_id, perm_id):
    """Manually adds a record to the table."""
    if not media.get(media_id):
        ctx.fail(click.style('No media found with id "{media_id}".', fg='red'))

    if not permission.get(perm_id):
        ctx.fail(click.style('No permission found with id "{perm_id}".', fg='red'))

    try:
        model.create(media_id, perm_id)
        ctx.invoke(list)
    except exception.DuplicatePermissionError:
        ctx.fail(click.style(f'Record with media_id "{media_id}" and perm_id "{perm_id}".', fg='read'))

@group.command('delete')
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """Manually deletes a record from the table."""
    click.echo(str(model.delete(id)) + ' record(s) deleted')
    ctx.invoke(list)

@group.command('update')
@click.argument('id')
@click.argument('media_id')
@click.argument('perm_id')
@click.pass_context
def update(ctx, id, media_id, perm_id):
    """Manually updates a record in the table."""
    try:
        model.update(id, media_id, perm_id)
        click.echo(click.style(f'Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.MediaPermNotFoundError:
        ctx.fail(click.style(f'Record with id "{id}", medai_id "{media_id}" and perm_id "{perm_id}" does not exist.', fg='red'))