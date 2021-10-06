PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS guest;
DROP TABLE IF EXISTS guest_media;
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
  default_sound INTEGER,
  default_color INTEGER,
  FOREIGN KEY (default_sound) REFERENCES sound (id)
  CONSTRAINT unique_full_name UNIQUE (first_name, last_name)
);

CREATE TABLE guest_media (
  id INTEGER PRIMARY KEY,
  guest_id INTEGER NOT NULL,
  media_id TEXT NOT NULL,
  sound INTEGER,
  color INTEGER,
  FOREIGN KEY (guest_id) REFERENCES guest (id) ON DELETE CASCADE,
  FOREIGN KEY (media_id) REFERENCES media (id) ON DELETE CASCADE,
  FOREIGN KEY (sound) REFERENCES sound (id)
  CONSTRAINT only_one_guest_for_media UNIQUE(media_id)
);

CREATE TABLE media (
  id TEXT PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  desc TEXT
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  desc TEXT
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
  name TEXT NOT NULL,
  last_update_timestamp TEXT DEFAULT (datetime('now', 'utc')) NOT NULL,
  content BLOB,
  CONSTRAINT unique_name UNIQUE (name)
);

CREATE TRIGGER UpdateLastUpdateTimestamp AFTER UPDATE OF name, content ON sound
BEGIN
  UPDATE sound SET last_update_timestamp = datetime('now', 'utc') WHERE id=NEW.id;
END
