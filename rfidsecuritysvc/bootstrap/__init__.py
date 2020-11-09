from rfidsecuritysvc.util.modules import call_method_on_each
import rfidsecuritysvc.bootstrap

def bootstrap(app):
  """Finds all the modules within this package and calls the bootstrap method on each."""
  call_method_on_each(rfidsecuritysvc.bootstrap, 'bootstrap', {'app': app}, None)
