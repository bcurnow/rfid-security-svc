import click
from flask.cli import AppGroup

from rfidsecuritysvc.cli.config import list
from rfidsecuritysvc.model import config
from rfidsecuritysvc.model.reader import RFID_DEVICE_CONFIG_KEY

group = AppGroup('reader')


def register(app):
    app.cli.add_command(group)


@group.command('set-device-name')
@click.argument('name')
@click.pass_context
def set_device_name(ctx, name):
    """Sets the appropriate config key for the reader device name"""
    c = config.get(RFID_DEVICE_CONFIG_KEY)
    if c:
        click.confirm(f'There is already a key "{c.key}" with value "{c.value}", do you want to replace with "{name}"?', abort=True)
        config.update(RFID_DEVICE_CONFIG_KEY, name)
    else:
        config.create(RFID_DEVICE_CONFIG_KEY, name)
    ctx.invoke(list)
