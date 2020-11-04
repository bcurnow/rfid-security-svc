from rfidsecuritysvc.db.dbms import get_db

def get(id):
  return get_db().execute('SELECT * FROM media WHERE id = ?', (id,)).fetchone()

def list():
  return get_db().execute('SELECT * FROM media ORDER BY id').fetchall()

def create(id, name, desc):
  db = get_db()
  db.execute('INSERT INTO media (id, name, desc) VALUES (?,?,?)', (id, name, desc))
  db.commit()

def delete(id):
  db = get_db()
  count = db.execute('DELETE FROM media WHERE id = ?', (id,)).rowcount
  db.commit()
  return count

def update(id, name, desc):
  db = get_db()
  count = db.execute('UPDATE media SET name = ?, desc = ? WHERE id = ?', (name, desc, id)).rowcount
  db.commit();
  return count
