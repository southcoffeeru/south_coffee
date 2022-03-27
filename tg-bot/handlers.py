from telegram import Update
from telegram.parsemode import ParseMode
from telegram.ext import CallbackContext

import database

from models import BotTask
from utils import format_message


def start(update: Update, context: CallbackContext):
    greeting: BotTask = database.session.query(BotTask).filter(
        BotTask.bot_task_type == 'greeting').first()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=format_message(
            greeting, update.message.from_user),
        parse_mode=ParseMode.MARKDOWN)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
