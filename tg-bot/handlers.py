from telegram import Update, User
from telegram.parsemode import ParseMode
from telegram.ext import CallbackContext
from sqlalchemy.exc import IntegrityError

import database
import logger

from models import BotTask, UserAccount
from utils import format_message


def start(update: Update, context: CallbackContext):
    user: User = update.message.from_user

    user_account = UserAccount(user_id=user.id, user_state='registered',
                               user_tg_first_name=user.first_name, user_tg_last_name=user.last_name, user_tg_nickname=user.name)
    try:
        session = database.session()
        session.add(user_account)
        session.commit()
        logger.logger.info('User {}({}) registered'.format(user.name, user.id))
    except IntegrityError:
        logger.logger.error(
            'User {}({}) already registered'.format(user.name, user.id))
    finally:
        session.rollback()

    greeting: BotTask = session.query(BotTask).filter(
        BotTask.bot_task_type == 'greeting').first()
    if greeting:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=format_message(
                greeting, user),
            parse_mode=ParseMode.MARKDOWN)
    else:
        logger.logger.error('No greetings messages found in bot tasks')


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
