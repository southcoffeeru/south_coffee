-- migrate:up

CREATE TYPE southcoffee.bot_task_type_enum AS ENUM ('greeting', 'match_message', 'feedback_message');

ALTER TABLE southcoffee.bot_task
    DROP COLUMN bot_task_type_id,
    ADD COLUMN bot_task_type southcoffee.bot_task_type_enum;

DROP TABLE southcoffee.bot_task_type;

-- migrate:down

CREATE  TABLE southcoffee.bot_task_type ( 
    bot_task_type_id     integer DEFAULT 0 NOT NULL  ,
    bot_task_type_name   varchar(100)  NOT NULL  ,
    CONSTRAINT pk_bot_task_type PRIMARY KEY ( bot_task_type_id )
);

ALTER TABLE southcoffee.bot_task
    DROP COLUMN bot_task_type,
    ADD COLUMN bot_task_type_id integer  NOT NULL,
    ADD CONSTRAINT fk_bot_task_bot_task_type FOREIGN KEY ( bot_task_type_id ) REFERENCES southcoffee.bot_task_type( bot_task_type_id );

DROP TYPE southcoffee.bot_task_type_enum;
