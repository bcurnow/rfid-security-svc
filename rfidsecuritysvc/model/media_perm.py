from rfidsecuritysvc.db import media_perm as table
from rfidsecuritysvc.model import BaseModel

class MediaPerm(BaseModel):
  def __init__(self, media_id, perm_id):
    self.media_id = media_id
    self.perm_id = perm_id

def get(id):
  row = table.get(id)
  if not row: return
  return __model(row)

def list():
  result = []
  for row in table.list():
    result.append(__model(row))
  return result  

def create(media_id, perm_id):
  return table.create(media_id, perm_id)

def delete(id):
  return table.delete(id)

def update(media_id, perm_id):
  return table.update(media_id, perm_id)

def __model(row):
  return MediaPerm(row['media_id'], row['perm_id'])
