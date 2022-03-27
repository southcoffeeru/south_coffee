# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ActionType(Base):
    __tablename__ = 'action_type'
    __table_args__ = {'schema': 'southcoffee', 'comment': 'dictionary of interactions'}

    action_type_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.action_type_action_type_id_seq'::regclass)"))
    action_type_name = Column(String(250), nullable=False)


class BotTask(Base):
    __tablename__ = 'bot_task'
    __table_args__ = {'schema': 'southcoffee', 'comment': 'dictionary of tasks for our bot'}

    bot_task_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.bot_task_bot_task_id_seq'::regclass)"))
    bot_task_name = Column(String(100), nullable=False)
    bot_task_title = Column(String(1000), nullable=False)
    bot_task_content = Column(String(1000), nullable=False)
    bot_task_type = Column(ENUM('greeting', 'match_message', 'feedback_message', name='bot_task_type_enum'))


class UserAccount(Base):
    __tablename__ = 'user_account'
    __table_args__ = {'schema': 'southcoffee', 'comment': 'users dictionary'}

    user_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.user_account_user_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_updated_at = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), server_default=text("NULL::character varying"))
    user_tg_username = Column(String(100))
    user_city = Column(String(100))
    user_type_of_activity = Column(String(1000))
    user_interests = Column(String(1000))
    user_attractiveness = Column(String(1000))
    user_others = Column(String(1000), server_default=text("NULL::character varying"))
    state_id = Column(Integer, nullable=False, server_default=text("0"))


class ActionLog(Base):
    __tablename__ = 'action_log'
    __table_args__ = {'schema': 'southcoffee'}

    action_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.action_log_action_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user_id = Column(ForeignKey('southcoffee.user_account.user_id'), nullable=False, index=True, server_default=text("0"))
    action_type_id = Column(ForeignKey('southcoffee.action_type.action_type_id'), nullable=False)
    bot_task_id = Column(ForeignKey('southcoffee.bot_task.bot_task_id'))
    action_text = Column(String(1000), nullable=False)

    action_type = relationship('ActionType')
    bot_task = relationship('BotTask')
    user = relationship('UserAccount')


class Button(Base):
    __tablename__ = 'button'
    __table_args__ = {'schema': 'southcoffee'}

    button_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.button_button_id_seq'::regclass)"))
    bot_task_id = Column(ForeignKey('southcoffee.bot_task.bot_task_id'), nullable=False)
    button_text = Column(String(250), nullable=False)
    button_url = Column(Integer, nullable=False)

    bot_task = relationship('BotTask')


class UsersMatch(Base):
    __tablename__ = 'users_match'
    __table_args__ = {'schema': 'southcoffee'}

    match_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.users_match_match_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user1_id = Column(ForeignKey('southcoffee.user_account.user_id'), nullable=False, server_default=text("0"))
    user2_id = Column(Integer, nullable=False, server_default=text("0"))

    user1 = relationship('UserAccount')


class UsersMeeting(Base):
    __tablename__ = 'users_meeting'
    __table_args__ = {'schema': 'southcoffee'}

    meeting_id = Column(Integer, primary_key=True, server_default=text("nextval('southcoffee.users_meeting_meeting_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    match_id = Column(ForeignKey('southcoffee.users_match.match_id'), nullable=False, server_default=text("0"))

    match = relationship('UsersMatch')
