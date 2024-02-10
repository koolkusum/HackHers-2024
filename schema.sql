DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    passw TEXT NOT NULL
);

CREATE TABLE tasks (
    TID INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    task TEXT NOT NULL,
    dateOfTask DATE NOT NULL
);