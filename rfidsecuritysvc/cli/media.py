import click
from flask.cli import AppGroup
from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.model import media as model

group = AppGroup('media')


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
@click.argument('id')
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def create(ctx, id, name, desc):
    """Manually adds a record to the table."""
    try:
        model.create(id, name, desc)
        ctx.invoke(list)
    except exception.DuplicateMediaError:
        ctx.fail(click.style(f'Record with id "{id}" or name "{name}" already exists.', fg='red'))


@group.command('delete')
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """Manually deletes a record from the table."""
    click.echo(click.style(f'{model.delete(id)} record(s) deleted.', bg='green', fg='black'))
    ctx.invoke(list)


@group.command('update')
@click.argument('id')
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def update(ctx, id, name, desc):
    """Manually updates a record in the table."""
    try:
        model.update(id, name, desc)
        click.echo(click.style('Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.MediaNotFoundError:
        ctx.fail(click.style(f'Record with id "{id}" does not exist.', fg='red'))
