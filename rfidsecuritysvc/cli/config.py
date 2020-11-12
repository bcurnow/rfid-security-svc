import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import config as model

group = AppGroup('config')


def register(app):
    app.cli.add_command(group)


@group.command('get')
@click.argument('key')
@click.pass_context
def get(ctx, key):
    """Gets a single record from the table."""
    record = model.get(key)
    if not record:
        ctx.fail(click.style(f'No record found with key "{key}".', fg='red'))

    click.echo(record.to_json())


@group.command('list')
def list():
    """List all the records in the table."""
    for i in model.list():
        click.echo(i.to_json())


@group.command('create')
@click.argument('key')
@click.argument('value')
@click.pass_context
def create(ctx, key, value):
    """Manually adds a record to the table."""
    try:
        model.create(key, value)
        ctx.invoke(list)
    except exception.DuplicateConfigError:
        ctx.fail(click.style(f'Record with key "{key}" already exists.', fg='red'))


@group.command('delete')
@click.argument('key')
@click.pass_context
def delete(ctx, key):
    """Manually deletes a record from the table."""
    click.echo(click.style(f'{model.delete(key)} record(s) deleted.', bg='green', fg='black'))
    ctx.invoke(list)


@group.command('update')
@click.argument('key')
@click.argument('value', required=False)
@click.pass_context
def update(ctx, key, value):
    """Manually updates a record in the table."""
    try:
        model.update(key, value)
        click.echo(click.style('Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.ConfigNotFoundError:
        ctx.fail(click.style(f'Record with key "{key}" does not exist.', fg='red'))
