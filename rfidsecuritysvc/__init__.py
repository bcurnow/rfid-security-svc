import os

from flask import Flask

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'rfidsecurity.sqlite'),
  )

  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)
  
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # Bootstrap rfidsecuritysvc
  from rfidsecuritysvc.bootstrap import main
  main.bootstrap(app)

  # Ensure that the database connection is closed when we teardown the appcontext
  from rfidsecuritysvc.db.dbms import close_db
  app.teardown_appcontext(close_db)

  return app
