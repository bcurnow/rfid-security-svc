from importlib import import_module
from pkgutil import iter_modules


def test_bootstrap_registers_cli_group(app):
    """This test will simply ensure that all the expected top-level groups are available, test code for each cli module will do the rest"""
    # First, iterate over the modules in cli and pull the command names so we make sure
    # we check them all as we add more over time
    import rfidsecuritysvc
    commands = []
    for module_info in iter_modules(path=rfidsecuritysvc.cli.__path__):
        module = import_module(f'{rfidsecuritysvc.cli.__name__}.{module_info.name}')
        commands.append(getattr(module, 'group').name)
    with app.app_context():
        for cmd in app.cli.list_commands(app.app_context()):
            assert cmd in commands
