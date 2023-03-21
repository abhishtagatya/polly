create table common_responses
(
    id         serial
        constraint common_response_pk
            primary key,
    lang_code  VARCHAR(2)  not null,
    event_name VARCHAR(20) unique not null,
    message    TEXT        not null
);

create table users
(
    id             int
        constraint users_pk
            primary key,
    name           VARCHAR(100),
    username       VARCHAR(100),
    messaging_lang VARCHAR(2),
    primary_lang   VARCHAR(2),
    learning_lang  VARCHAR(2)
);

create unique index users_username_uindex
    on users (username);

create table conversations
(
    id            serial
        constraint conversations_pk
            primary key,
    user_message  TEXT,
    chat_response TEXT,
    column_4      int
);
