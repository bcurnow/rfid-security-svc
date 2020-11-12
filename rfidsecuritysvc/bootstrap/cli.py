import rfidsecuritysvc.cli
from rfidsecuritysvc.util.modules import call_method_on_each


def bootstrap(app):
    """Will call the register method on each module to register their commands"""
    call_method_on_each(rfidsecuritysvc.cli, 'register', {'app': app})
