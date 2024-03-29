import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import media_perm as model

group = AppGroup('media-perm')


def register(app):
    app.cli.add_command(group)


@group.command('get')
@click.argument('id', type=int)
@click.pass_context
def get(ctx, id):
    """Gets a single record from the table."""
    record = model.get(id)
    if not record:
        ctx.fail(click.style(f'No record found with id "{id}".', fg='red'))

    click.echo(record.to_json())


@group.command('list')
@click.argument('media_id', required=False)
def list(media_id):
    """List all the records in the table."""
    if media_id:
        results = model.list(media_id)
    else:
        results = model.list()

    for i in results:
        click.echo(i.to_json())


@group.command('create')
@click.argument('media_id')
@click.argument('permission_id', type=int)
@click.pass_context
def create(ctx, media_id, permission_id):
    """Manually adds a record to the table."""
    try:
        model.create(media_id, permission_id)
        ctx.invoke(list)
    except exception.DuplicateMediaPermError:
        ctx.fail(click.style(f'Record with media_id "{media_id}" and permission_id "{permission_id}" already exists.', fg='red'))
    except exception.MediaNotFoundError:
        ctx.fail(click.style(f'No media found with id "{media_id}".', fg='red'))
    except exception.PermissionNotFoundError:
        ctx.fail(click.style(f'No permission found with id "{permission_id}".', fg='red'))


@group.command('delete')
@click.argument('id', type=int)
@click.pass_context
def delete(ctx, id):
    """Manually deletes a record from the table."""
    click.echo(click.style(str(model.delete(id)) + ' record(s) deleted.', bg='green', fg='black'))
    ctx.invoke(list)


@group.command('update')
@click.argument('id', type=int)
@click.argument('media_id')
@click.argument('permission_id', type=int)
@click.pass_context
def update(ctx, id, media_id, permission_id):
    """Manually updates a record in the table."""
    try:
        model.update(id, media_id, permission_id)
        click.echo(click.style('Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.MediaPermNotFoundError:
        ctx.fail(click.style(f'Record with id "{id}", media_id "{media_id}" and permission_id "{permission_id}" does not exist.', fg='red'))
