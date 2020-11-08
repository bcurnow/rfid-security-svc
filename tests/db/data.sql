-- The value below creates an ADMIN_API_KEY value of 'test'
INSERT INTO config (key, value) 
VALUES 
  ('ADMIN_API_KEY', 'pbkdf2:sha256:150000$eSZubwQx$69e8839977e1461e7384a0a45a2d11e20a11ff7e0f6ade95c8b60f4b2893bbd0');

INSERT INTO media (id, name, desc)
VALUES 
  ('test media 1', 'test media 1', 'Media for testing (1)'),
  ('test media 2', 'test media 2', 'Media for testing (2)'),
  ('test media 3', 'test media 3', 'Media for testing (3)'),
  ('test media 4', 'test media 4', 'Media for testing (4)'),
  ('test media 5', 'test media 5', 'Media for testing (5)'),
  ('test open door', 'test open door', 'This media will be assigned the permission Open Door');

-- Make sure to leave Open Door at the top so the media_perm inserts work too
INSERT INTO permission (name, desc)
VALUES
  ('Open Door', 'Opens the door'),
  ('Perm 1', 'Permission 1'),
  ('Perm 2', 'Permission 2'),
  ('Perm 3', 'Permission 3'),
  ('Perm 4', 'Permission 4'),
  ('Perm 5', 'Permission 5');

-- Insert a record granting the test open door media the Open Door permission
INSERT INTO media_perm(media_id, perm_id)
VALUES
  ('test open door', '1');
