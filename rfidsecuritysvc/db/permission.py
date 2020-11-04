from rfidsecuritysvc.db.dbms import get_db

def get(id):
  return get_db().execute('SELECT * FROM permission WHERE id = ?', (id,)).fetchone()

def list():
  return get_db().execute('SELECT * FROM permission ORDER BY id').fetchall()

def create(name, desc):
  db = get_db()
  db.execute('INSERT INTO permission (name, desc) VALUES (?,?)', (name, desc))
  db.commit()

def delete(id):
  db = get_db()
  count = db.execute('DELETE FROM permission WHERE id = ?', (id,)).rowcount
  db.commit()
  return count

def update(id, name, desc):
  db = get_db()
  count = db.execute('UPDATE permission SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount
  db.commit();
  return count
