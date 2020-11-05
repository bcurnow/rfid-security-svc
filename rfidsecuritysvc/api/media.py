from rfidsecuritysvc.model import media

def get(media_id):
  m = media.get(media_id)
  if m: return m.to_json()
  return f"No media with id '{media_id}'.", 404
