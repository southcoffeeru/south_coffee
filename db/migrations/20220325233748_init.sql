-- migrate:up

CREATE SCHEMA IF NOT EXISTS southcoffee;

CREATE  TABLE southcoffee.action_type ( 
	action_type_id       serial NOT NULL  ,
	action_type_name     varchar(250)  NOT NULL  ,
	CONSTRAINT pk_action_type PRIMARY KEY ( action_type_id )
 );

CREATE  TABLE southcoffee.bot_task_type ( 
	bot_task_type_id     serial NOT NULL  ,
	bot_task_type_name   varchar(100)  NOT NULL  ,
	CONSTRAINT pk_bot_task_type PRIMARY KEY ( bot_task_type_id )
 );

CREATE  TABLE southcoffee.user_account ( 
	user_id              serial NOT NULL  ,
	created_at           timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	last_updated_at      timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	user_name            varchar(100)  NOT NULL  ,
	user_email           varchar(100) DEFAULT NULL::character varying   ,
	user_tg_username     varchar(100)    ,
	user_city            varchar(100)    ,
	user_type_of_activity varchar(1000)    ,
	user_interests       varchar(1000)    ,
	user_attractiveness  varchar(1000)    ,
	user_others          varchar(1000) DEFAULT NULL::character varying   ,
	state_id             integer DEFAULT 0 NOT NULL  ,
	CONSTRAINT pk_users PRIMARY KEY ( user_id )
 );

CREATE  TABLE southcoffee.users_match ( 
	match_id             serial NOT NULL  ,
	created_at           timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	user1_id             integer DEFAULT 0 NOT NULL  ,
	user2_id             integer DEFAULT 0 NOT NULL  ,
	CONSTRAINT pk_users_match PRIMARY KEY ( match_id ),
	CONSTRAINT fk_users_match_user FOREIGN KEY ( user1_id ) REFERENCES southcoffee.user_account( user_id )   
 );

CREATE  TABLE southcoffee.users_meeting ( 
	meeting_id           serial NOT NULL  ,
	created_at           timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	match_id             integer DEFAULT 0 NOT NULL  ,
	CONSTRAINT pk_users_meetings PRIMARY KEY ( meeting_id ),
	CONSTRAINT fk_users_meetings_users_match FOREIGN KEY ( match_id ) REFERENCES southcoffee.users_match( match_id )   
 );

CREATE  TABLE southcoffee.bot_task ( 
	bot_task_id          serial  NOT NULL  ,
	bot_task_name        varchar(100),
	bot_task_title       varchar(1000)  NOT NULL  ,
	bot_task_content     varchar(1000)  NOT NULL  ,
	bot_task_type_id     integer  NOT NULL  ,
	CONSTRAINT pk_bot_task PRIMARY KEY ( bot_task_id ),
	CONSTRAINT fk_bot_task_bot_task_type FOREIGN KEY ( bot_task_type_id ) REFERENCES southcoffee.bot_task_type( bot_task_type_id )   
 );

CREATE  TABLE southcoffee.button ( 
	button_id            serial  NOT NULL  ,
	bot_task_id          integer  NOT NULL  ,
	button_text          varchar(250)  NOT NULL  ,
	button_url           integer  NOT NULL  ,
	CONSTRAINT pk_button PRIMARY KEY ( button_id ),
	CONSTRAINT fk_button_bot_task FOREIGN KEY ( bot_task_id ) REFERENCES southcoffee.bot_task( bot_task_id )   
 );

CREATE  TABLE southcoffee.action_log ( 
	action_id            serial NOT NULL  ,
	created_at           timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	user_id              integer DEFAULT 0 NOT NULL  ,
	action_type_id       integer  NOT NULL  ,
	bot_task_id          integer    ,
	action_text          varchar(1000)  NOT NULL  ,
	CONSTRAINT pk_activity_log PRIMARY KEY ( action_id ),
	CONSTRAINT fk_action_log_action_type FOREIGN KEY ( action_type_id ) REFERENCES southcoffee.action_type( action_type_id )   ,
	CONSTRAINT fk_action_log_bot_task FOREIGN KEY ( bot_task_id ) REFERENCES southcoffee.bot_task( bot_task_id )   ,
	CONSTRAINT fk_activity_log_user FOREIGN KEY ( user_id ) REFERENCES southcoffee.user_account( user_id )   
 );

CREATE INDEX idx_activity_log_user_id ON southcoffee.action_log ( user_id );

COMMENT ON TABLE southcoffee.action_type IS 'dictionary of interactions';

COMMENT ON TABLE southcoffee.user_account IS 'users dictionary';

COMMENT ON TABLE southcoffee.bot_task IS 'dictionary of tasks for our bot';


-- migrate:down

DROP INDEX southcoffee.idx_activity_log_user_id;
DROP TABLE southcoffee.action_log;
DROP TABLE southcoffee.button;
DROP TABLE southcoffee.bot_task;
DROP TABLE southcoffee.users_meeting;
DROP TABLE southcoffee.users_match;
DROP TABLE southcoffee.user_account;
DROP TABLE southcoffee.bot_task_type;
DROP TABLE southcoffee.action_type;

DROP SCHEMA southcoffee;