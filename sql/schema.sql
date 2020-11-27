-- schema.sql defines the schema or data layout of the database
-- Note: CASCADE makes corresponding changes upon delete/update
PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username VARCHAR(20) NOT NULL PRIMARY KEY,
);

-- username1 follows username2
CREATE TABLE following( 
  username1 VARCHAR(20) NOT NULL,
  username2 VARCHAR(20) NOT NULL,
  PRIMARY KEY (username1, username2),
  FOREIGN KEY (username1) REFERENCES users(username)
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
  FOREIGN KEY (username2) REFERENCES users(username)
    ON UPDATE CASCADE 
    ON DELETE CASCADE
);