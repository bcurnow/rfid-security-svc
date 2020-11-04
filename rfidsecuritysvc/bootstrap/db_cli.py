import rfidsecuritysvc.db.cli
from rfidsecuritysvc.util.modules import call_method_on_each
from flask.cli import AppGroup

def bootstrap(app):
  """Will register each cli module with a base group."""
  base_group = AppGroup('db')
  call_method_on_each(rfidsecuritysvc.db.cli, 'register', {'app': app, 'parent': base_group})
  app.cli.add_command(base_group)
