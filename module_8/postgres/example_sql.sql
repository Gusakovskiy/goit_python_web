CREATE TABLE table_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE table_user ADD COLUMN email TEXT;

INSERT INTO table_user(name, email)
VALUES ('VASYA', 'VASYA@GMAIL.com')
RETURNING *;

DROP TABLE table_user;
--- NEXT