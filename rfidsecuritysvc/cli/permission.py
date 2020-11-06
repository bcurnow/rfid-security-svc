import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import permission as model

group = AppGroup('permission')

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
@click.argument('name')
@click.argument('desc', required=False)
@click.pass_context
def create(ctx, name, desc):
    """Manually adds a record to the table."""
    try:
        model.create(name, desc)
        ctx.invoke(list)
    except exception.DuplicatePermissionError:
        ctx.fail(click.style(f'Record with name "{name}" already exists.', fg='red'))

@group.command('delete')
@click.argument('id')
@click.pass_context
def delete(ctx, id):
    """Manually deletes a record from the table."""
    click.echo(click.style(f'{model.delete(id)} record(s) deleted', bg='green', fg='black'))
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
        click.echo(click.style(f'Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.PermissionNotFoundError:
        ctx.fail(click.style(f'Record with name "{name}" does not exist.', fg='red'))
