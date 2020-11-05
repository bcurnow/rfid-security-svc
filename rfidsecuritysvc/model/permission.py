from rfidsecuritysvc.db import permission as table
from rfidsecuritysvc.model import BaseModel

class Permission(BaseModel):
  def __init__(self, id, name, desc=None):
    self.id = id
    self.name = name
    self.desc = desc

def get(id):
  row = table.get(id)
  if not row: return
  return __model(row)

def list():
  result = []
  for row in table.list():
    result.append(__model(row))
  return result  

def create(name, desc):
  return table.create(name, desc)

def delete(id):
  return table.delete(id)

def update(id, name, desc):
  return table.update(id, name, desc)

def __model(row):
  return Permission(row['id'], row['name'], row['desc'])
