import click
from flask.cli import AppGroup
from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.model import guest as model

group = AppGroup('guest')


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
def list():
    """List all the records in the table."""
    for i in model.list():
        click.echo(i.to_json())


@group.command('create')
@click.argument('first_name')
@click.argument('last_name')
@click.argument('sound', type=int, required=False)
@click.argument('color', type=int, required=False)
@click.pass_context
def create(ctx, first_name, last_name, sound, color):
    """Manually adds a record to the table."""
    try:
        model.create(first_name, last_name, sound, color)
        ctx.invoke(list)
    except exception.DuplicateGuestError:
        ctx.fail(click.style(f'Record with first_name "{first_name}" and last_name "{last_name}" already exists.', fg='red'))


@group.command('delete')
@click.argument('id', type=int)
@click.pass_context
def delete(ctx, id):
    """Manually deletes a record from the table."""
    click.echo(click.style(f'{model.delete(id)} record(s) deleted.', bg='green', fg='black'))
    ctx.invoke(list)


@group.command('update')
@click.argument('id', type=int)
@click.argument('first_name')
@click.argument('last_name')
@click.argument('sound', type=int, required=False)
@click.argument('color', type=int, required=False)
@click.pass_context
def update(ctx, id, first_name, last_name, sound, color):
    """Manually updates a record in the table."""
    try:
        model.update(id, first_name, last_name, sound, color)
        click.echo(click.style('Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.GuestNotFoundError:
        ctx.fail(click.style(f'Record with id "{id}" does not exist.', fg='red'))
