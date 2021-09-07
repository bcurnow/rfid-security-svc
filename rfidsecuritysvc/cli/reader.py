import click
from flask.cli import AppGroup

from rfidsecuritysvc.cli.config import list
from rfidsecuritysvc.model import config
from rfidsecuritysvc.model.reader import RFID_SERVICE_URL_CONFIG_KEY

group = AppGroup('reader')


def register(app):
    app.cli.add_command(group)


@group.command('set-url')
@click.argument('url')
@click.option('--yes', is_flag=True)
@click.pass_context
def set_url(ctx, url, yes):
    """Sets the appropriate config key for the reader URL"""
    c = config.get(RFID_SERVICE_URL_CONFIG_KEY)
    if c:
        if not yes:
            click.confirm(f'There is already a key "{c.key}" with value "{c.value}", do you want to replace with "{url}"?', abort=True)
        config.update(RFID_SERVICE_URL_CONFIG_KEY, url)
    else:
        config.create(RFID_SERVICE_URL_CONFIG_KEY, url)
    ctx.invoke(list)
