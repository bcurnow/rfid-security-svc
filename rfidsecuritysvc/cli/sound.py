import os

import click
from flask.cli import AppGroup
import rfidsecuritysvc.exception as exception
from rfidsecuritysvc.model import sound as model

group = AppGroup('sound')


def register(app):
    app.cli.add_command(group)


@group.command('get')
@click.argument('name')
@click.argument('output_file', type=click.File('wb'), required=False)
@click.pass_context
def get(ctx, name, output_file):
    """Gets a single record from the table."""
    record = model.get(name)
    if not record:
        ctx.fail(click.style(f'No record found with name "{name}".', fg='red'))

    if output_file:
        output_file.write(record.content)
        click.echo(f'{name} was saved to {os.path.abspath(output_file.name)}')
    else:
        click.echo(record.to_json())


@group.command('list')
def list():
    """List all the records in the table."""
    for i in model.list():
        click.echo(i.to_json())


@group.command('create')
@click.argument('name')
@click.argument('input_file', type=click.File('rb'))
@click.pass_context
def create(ctx, name, input_file):
    """Manually adds a record to the table."""
    try:
        model.create(name, input_file.read())
        ctx.invoke(list)
    except exception.DuplicateSoundError:
        ctx.fail(click.style(f'Record with name "{name}" already exists.', fg='red'))


@group.command('delete')
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """Manually deletes a record from the table."""
    click.echo(click.style(f'{model.delete(name)} record(s) deleted.', bg='green', fg='black'))
    ctx.invoke(list)


@group.command('update')
@click.argument('id')
@click.argument('name')
@click.argument('input_file', type=click.File('rb'), required=False)
@click.pass_context
def update(ctx, id, name, input_file):
    """Manually updates a record in the table."""
    try:
        if input_file is None:
            model.update(id, name)
        else:
            model.update(id, name, input_file.read())
        click.echo(click.style('Record updated.', bg='green', fg='black'))
        ctx.invoke(list)
    except exception.SoundNotFoundError:
        ctx.fail(click.style(f'Record with id "{id}" does not exist.', fg='red'))
