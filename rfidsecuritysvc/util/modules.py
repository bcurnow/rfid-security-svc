from pkgutil import iter_modules
from importlib import import_module


def call_method_on_each(package, method_name, method_args, module_filter=None):
    """Execute the specified method name passing the specified arguments on all modules in the specified package that match the filter."""
    for module_info in iter_modules(path=package.__path__):
        if module_filter and not (module_filter(module_info.name)):
            pass
        else:
            module = import_module(f'{package.__name__}.{module_info.name}')
            getattr(module, method_name)(**method_args)
