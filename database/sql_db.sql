create table if not exists menu (
id integer primary key autoincrement,
title text not null,
url text not null
);

create table if not exists teachermenu (
id integer primary key autoincrement,
title text not null,
url text not null
);

create table if not exists studentmenu (
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
nick text not null,
password text not null,
age integer not null,
name text null,
status text not null
);