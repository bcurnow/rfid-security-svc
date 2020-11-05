from rfidsecuritysvc.db.dbms import close_db

def bootstrap(app):
  """ Ensure that the database connection is closed when we teardown the appcontext"""
  app.teardown_appcontext(close_db)
