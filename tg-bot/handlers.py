from typing import List
from telegram import Update, User
from telegram.ext import CallbackContext
from sqlalchemy.exc import IntegrityError

import database
import logger

from models import BotTask, UserAccount, UsersMatch
from utils import send_formated_message
from handlers_utils import admin_handler, message_handler


def start(update: Update, context: CallbackContext):
    user: User = update.message.from_user

    user_account = UserAccount(user_id=user.id,
                               user_state='registered',
                               user_tg_first_name=user.first_name,
                               user_tg_last_name=user.last_name,
                               user_tg_nickname=user.name)
    try:
        session = database.session()
        session.add(user_account)
        session.commit()
        logger.logger.info('User {}({}) registered'.format(user.name, user.id))
    except IntegrityError:
        logger.logger.error(
            'User {}({}) already registered'.format(user.name, user.id))
        session.rollback()

    greeting: BotTask = session.query(BotTask).filter(
        BotTask.bot_task_type == 'greeting').first()
    if greeting:
        send_formated_message(context, update.effective_chat.id,
                              'greeting', tg_user=user, db_user=user_account)
    else:
        logger.logger.error('No greetings messages found in bot tasks')


@admin_handler
def create_match(update: Update, context: CallbackContext):
    message = 'Unknown error!'
    if len(context.args) != 2:
        message = 'Error! You should specify exaclty two user ids'
        return message_handler(update, context, message)

    users_ids = []
    for id in context.args:
        try:
            users_ids.append(int(id))
        except ValueError:
            print('Please enter an integer')
            message = 'Error! Both ids should be integers'
            return message_handler(update, context, message)

    session = database.session()
    users: List[UserAccount] = [session.query(UserAccount).filter(
        UserAccount.user_id == x).first() for x in context.args]

    if not users[0]:
        message = 'User {} not found'.format(context.args[0])
        return message_handler(update, context, message)
    elif not users[1]:
        message = 'User {} not found'.format(context.args[1])
        return message_handler(update, context, message)

    match = UsersMatch(user1_id=users[0].user_id, user2_id=users[1].user_id)
    try:
        session.add(match)
        session.commit()
        message = 'Match for {} and {} created successfully'.format(
            users[0].user_id, users[1].user_id)

        logger.logger.info(message)
    except:
        message = 'Error! Could not create match in database for users {} and {}'.format(
            users[0].user_id, users[1].user_id)
        logger.logger.error(message)
        session.rollback()

    return message_handler(update, context, message)
