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

create table if not exists users (
id integer primary key autoincrement,
firstname text not null,
secondname text not null,
thirdname text not null,
age integer not null,
status text not null
);