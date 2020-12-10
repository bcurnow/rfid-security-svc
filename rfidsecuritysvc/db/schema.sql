PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS guest_media;
DROP TABLE IF EXISTS guest_perm;
DROP TABLE IF EXISTS guest_pref;
DROP TABLE IF EXISTS media;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS sound;
DROP TABLE IF EXISTS media_perm;

CREATE TABLE config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE guest (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  CONSTRAINT unique_full_name UNIQUE (first_name, last_name)
);

CREATE TABLE media (
  id TEXT PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  desc TEXT
);

CREATE TABLE guest_media (
  id INTEGER PRIMARY KEY,
  guest_id INTEGER NOT NULL,
  media_id TEXT NOT NULL,
  FOREIGN KEY (guest_id) REFERENCES guest (id) ON DELETE CASCADE,
  FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  desc TEXT
);

CREATE TABLE guest_perm (
  id INTEGER PRIMARY KEY,
  guest_id INTEGER NOT NULL,
  perm_id INTEGER NOT NULL,
  FOREIGN KEY (guest_id) REFERENCES guest (id) ON DELETE CASCADE,
  FOREIGN KEY (perm_id) REFERENCES permission (id) ON DELETE CASCADE,
  CONSTRAINT unique_guest_perm UNIQUE (guest_id, perm_id)
);

CREATE TABLE guest_pref (
  name TEXT PRIMARY KEY,
  guest_id INTEGER NOT NULL,
  value TEXT NOT NULL,
  FOREIGN KEY (guest_id) REFERENCES guest (id) ON DELETE CASCADE,
  CONSTRAINT unique_guest_pref UNIQUE (name, guest_id)
);

CREATE TABLE media_perm (
  id INTEGER PRIMARY KEY,
  media_id TEXT NOT NULL,
  perm_id INTEGER NOT NULL,
  FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE,
  FOREIGN KEY (perm_id) REFERENCES permission (id) ON DELETE CASCADE,
  CONSTRAINT unique_association UNIQUE (media_id, perm_id)
);

CREATE TABLE sound (
  id INTEGER PRIMARY KEY,
  data BLOB,
  file_name TEXT NOT NULL,
  CONSTRAINT unique_file_name UNIQUE (file_name)
);
