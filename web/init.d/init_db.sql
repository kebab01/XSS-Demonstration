create table if not exists users(
    username text primary key not null unique,
    password text not null, -- Yes this is very bad
    avatar text  not null
);

create table if not exists posts(
    id integer generated always as identity primary key,
    title text not null,
    author text not null references users,
    content text not null
)