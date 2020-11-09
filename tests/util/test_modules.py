import os
import sys
import pkgutil
import importlib.machinery
import importlib.util
from importlib import import_module

from rfidsecuritysvc.util.modules import call_method_on_each

def test_call_method_on_each_calls_each():
    package = __import_testmod()
    import testmod.call_method_on_each as one
    import testmod.call_method_on_each2 as two

    # Reset to uncalled sdtate
    one.called = False
    two.called = False

    call_method_on_each(package, 'test', {})

    assert one.called == True
    assert two.called == True

def __import_testmod():
    # Because of the way python works, we need to do a bit of trickery to makek the testmod available
    # First, determine the absolute path to the testmod directory
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testmod'))

    # Import the __init__.py file as a module to serve as the package
    package = __load_from_path('testmod', os.path.join(module_path, '__init__.py'))

    #modules = []
    #for mod_name in ['call_method_on_each', 'call_method_on_each2']:
#    return (package, modules)  
    return package

def __load_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

    
