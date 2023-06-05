create table if not exists menu (
id integer primary key autoincrement,
title text not null,
url text not null
);

create table if not exists game (
id integer primary key autoincrement,
title text not null,
info text not null,
url text not null
);

create table if not exists users (
id integer primary key autoincrement,
nick text not null unique,
password text not null,
age integer not null,
name text null unique,
status text not null
);

create table if not exists reports (
id integer primary key autoincrement,
user text not null,
about text not null,
time integer not null,
name text null unique,
status text not null
);

create table if not exists answers (
id integer primary key autoincrement,
user text not null,
text text not null,
idrep integer not null,
time integer not null
);

create table if not exists contact (
id integer primary key autoincrement,
user text not null,
title text not null unique,
text text not null,
time integer not null
);