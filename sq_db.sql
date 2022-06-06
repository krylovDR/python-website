CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
psw text NOT NULL,
isadmin integer NOT NULL,
lab0 text NOT NULL,
lab1 text NOT NULL,
lab2 text NOT NULL,
lab3 text NOT NULL,
lab4 text NOT NULL,
lab5 text NOT NULL,
lab6 text NOT NULL
);