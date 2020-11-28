-- schema.sql defines the schema or data layout of the database
-- Note: CASCADE makes corresponding changes upon delete/update
PRAGMA foreign_keys = ON;

-- user
CREATE TABLE users(
  username VARCHAR(20) NOT NULL PRIMARY KEY
);

-- username1 follows username2
CREATE TABLE following( 
  username1 VARCHAR(20) NOT NULL,
  username2 VARCHAR(20) NOT NULL,
  PRIMARY KEY (username1, username2),
  FOREIGN KEY (username1) REFERENCES users(username)
    ON UPDATE CASCADE 
    ON DELETE CASCADE
);

CREATE TABLE toptracks(
  username VARCHAR(20) NOT NULL,
  track VARCHAR(20) NOT NULL,
  rank NUMBER NOT NULL,
  PRIMARY KEY (username, track),
  FOREIGN KEY (username) REFERENCES users(username)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE topartists(
  username VARCHAR(20) NOT NULL,
  artist VARCHAR(20) NOT NULL,
  rank NUMBER NOT NULL,
  PRIMARY KEY (username, artist),
  FOREIGN KEY (username) REFERENCES users(username)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);