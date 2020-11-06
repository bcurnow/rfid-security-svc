DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS media_perm;
DROP TABLE IF EXISTS media;
DROP TABLE IF EXISTS permission;

CREATE TABLE config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE media (
  id TEXT PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  desc TEXT
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  desc TEX 
);

CREATE TABLE media_perm (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  media_id TEXT NOT NULL,
  perm_id INTEGER NOT NULL,
  FOREIGN KEY (media_id) REFERENCES media (id),
  FOREIGN KEY (perm_id) REFERENCES permission (id),
  CONSTRAINT unique_association UNIQUE (media_id, perm_id)
);
