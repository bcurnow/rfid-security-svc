import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import sound as model

group = AppGroup('sound')


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
@click.argument('file_name')
@click.argument('input_file', type=click.File('rb'))
@click.pass_context
def create(ctx, file_name, input_file):
    """Manually adds a record to the table."""
    try:
        model.create(file_name, input_file.read())
        ctx.invoke(list)
    except exception.DuplicateSoundError:
        ctx.fail(click.style(f'Record with file name "{file_name}" already exists.', fg='red'))


@group.command('delete')
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """Manually deletes a record from the table."""
    click.echo(click.style(f'{model.delete(id)} record(s) deleted.', bg='green', fg='black'))
    ctx.invoke(list)


@group.command('update')
@click.argument('id')
@click.argument('file_name')
@click.pass_context
def update(ctx, id, file_name):
    """Manually updates a record in the table."""
    try:
        model.update(id, file_name)
        click.echo(click.style('Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.SoundNotFoundError:
        ctx.fail(click.style(f'Record with id "{id}" does not exist.', fg='red'))
