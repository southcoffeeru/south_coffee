from telegram import Update
from telegram.ext import CallbackContext

import database

from models import Message


def start(update: Update, context: CallbackContext):
    greeting : Message = database.session.query(Message).filter(Message.id == 1)[0]
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=greeting.message)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
