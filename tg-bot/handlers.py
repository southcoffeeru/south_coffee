from telegram import Update, User
from telegram.parsemode import ParseMode
from telegram.ext import CallbackContext

import database
import logger

from models import BotTask, UserAccount
from utils import format_message

def start(update: Update, context: CallbackContext):
    user : User = update.message.from_user

    user_account = UserAccount(user_id=user.id, user_state='registered')
    database.session.add(user_account)
    database.session.commit()

    greeting: BotTask = database.session.query(BotTask).filter(
        BotTask.bot_task_type == 'greeting').first()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=format_message(
            greeting, user),
        parse_mode=ParseMode.MARKDOWN)
    logger.logger.info('user {}({}) registered'.format(user.name, user.id))


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
