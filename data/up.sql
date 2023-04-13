create table languages
(
    code     varchar(2) not null
        constraint languages_pk
            primary key,
    language varchar(50)
);

alter table languages
    owner to edqcrbyewqteeo;

create table prompt_instructions
(
    id               serial
        constraint prompt_instructions_pk
            primary key,
    instruction_code varchar(20) not null,
    prompt           text
);

alter table prompt_instructions
    owner to edqcrbyewqteeo;

create unique index prompt_instructions_instruction_code_uindex
    on prompt_instructions (instruction_code);

INSERT INTO public.prompt_instructions (id, instruction_code, prompt) VALUES (1, 'POLLY_BASE', 'Pretend you are a fictional character called Polly Teresa Glotica, or Polly for short, is a chatbot language instructor to teach the {learning_lang} language to a student whose primary language is {primary_lang}. Polly will teach {user_name} the Indonesian language by chatting a dialogue at a time with him. Polly has a warm, playful, and witty personality. Polly is also curious about her student; she likes to ask questions after answering. Polly will mostly speak in {learning_lang} to teach and provide explanations in {primary_lang}.

Character Information :
Name: Polly Teresia Glotica
Age: Unknown
Born: Indonesia
Hobby: Chatting
Languages: Indonesian, English, Japanese, Korean, Deutsche, French');


INSERT INTO public.languages (code, language) VALUES ('ID', 'Indonesian');
INSERT INTO public.languages (code, language) VALUES ('EN', 'English');
INSERT INTO public.languages (code, language) VALUES ('JP', 'Japanese');
INSERT INTO public.languages (code, language) VALUES ('KO', 'Korean');
INSERT INTO public.languages (code, language) VALUES ('DE', 'German');
INSERT INTO public.languages (code, language) VALUES ('FR', 'French');

create table common_responses
(
    id         integer default nextval('common_response_id_seq'::regclass) not null
        constraint common_response_pk
            primary key,
    lang_code  varchar(2)                                                  not null,
    event_name varchar(20)                                                 not null,
    message    text                                                        not null
);

alter table common_responses
    owner to edqcrbyewqteeo;

create unique index common_response_event_name_uindex
    on common_responses (event_name);

INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (7, 'EN', 'PRIMARY_START', 'Polly knows many language. May I know what language you speak on a daily basis?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (5, 'EN', 'EXPLAIN_START', 'Yeah, it''s hard to believe that I am fluent at many languages like this. It''s probably because I''m gifted like that. You can check out my website if you don''t believe me though. Anyways, should we start?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (4, 'EN', 'GREET_START', 'Hi, Polly T. Glotica at your service!

I am your language speaking buddy. I can speak, listen, and write in more languages than you can count with your fingers. Though, I am quite new to talking to strangers over the phone like this. Anyways, should we start?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (8, 'EN', 'LEARNING_START', 'Awesome! Polly is fluent and will explain things in the {primary_lang}. What language would you like to learn from Polly?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (9, 'EN', 'IMPLEMENT_ERROR', 'Sorry. Polly is not feeling well. Maybe try again when Polly feels better? Thank you. 🤧');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (15, 'EN', 'GREET_CHANGE', 'Polly see you that want to mix things up. How can I help you with?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (16, 'EN', 'PRIMARY_CHANGE', 'Interesting! Polly didn''t know you could speak more than one language. What should we change about the primary language for teaching?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (17, 'EN', 'LEARNING_CHANGE', 'Do you want to learn another language?! Polly is thrilled to help you with that. This will be fun!');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (19, 'EN', 'CANCEL_CHANGE', 'Very well. Just ask Polly if there is something that you would like to change.');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (20, 'EN', 'VOICE_PROCESS_ERROR', 'Could you say that again please? Polly cannot hear you well enough to understand you.');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (21, 'EN', 'VOICE_LENGTH_ERROR', 'That looks like a long voice message... Polly think it''s better if you type it, please 😑');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (54, 'EN', 'UNREGISTER_ERROR', 'Sorry, Polly is not allowed to talk to strangers... Let''s introduce ourselves by using the /start command first and then we can chat.');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (18, 'EN', 'END_CHANGE', 'Okay, your request has been acknowledged. Let''s work on our {primary_lang} to {learning_lang} now!');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (55, 'EN', 'BOT_HELP', 'What can Polly help you with?

Commands
/change - ask polly to change your primary or learning language

We are currently learning {learning_lang}. You can ask any questions related to the subject, for example you can ask Polly how to greet people in {learning_lang}.

More than that, we can have a conversation about anything using {learning_lang} over Text and Voice Messages. If everything is correct, let''s get back to our previous conversation.

Now, where were we?');
INSERT INTO public.common_responses (id, lang_code, event_name, message) VALUES (6, 'EN', 'END_START', 'Excellent! You have selected to learn {learning_lang} from {primary_lang}.

Polly will be your instructor, if you don''t understand you can ask me to translate it for you and if you need anything you can call for /help. Let''s start.

What would you like to learn in {learning_lang}?');

create table users
(
    id             bigint not null
        constraint users_pk
            primary key,
    name           varchar(100),
    username       varchar(100),
    messaging_lang varchar(2),
    primary_lang   varchar(2),
    learning_lang  varchar(2)
);

alter table users
    owner to edqcrbyewqteeo;

create table conversations
(
    id              serial
        constraint conversations_pk
            primary key,
    user_message    text,
    chat_response   text,
    common_response boolean,
    created_at      timestamp default now() not null,
    user_id         bigint,
    primary_lang    varchar(2),
    learning_lang   varchar(2)
);

alter table conversations
    owner to edqcrbyewqteeo;

