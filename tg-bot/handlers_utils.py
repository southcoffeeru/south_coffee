import database
import logger

from telegram import Update, User
from telegram.ext import CallbackContext

from models import UserAccount


def admin_handler(handler):
    def wrap(update: Update, context: CallbackContext):
        if not update.message:
            logger.logger.error(
                'Unsupported update type for admin handler {}'.format(handler.__name__))
            return
        user: User = update.message.from_user

        session = database.session()
        user_account: UserAccount = session.query(UserAccount).filter(
            UserAccount.user_id == user.id).first()

        if user_account and user_account.user_role == 'admin':
            return handler(update, context)
        return __accerss_error(update, context)

    def __accerss_error(update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Oops! You don\'t have admin permissions ')
        pass

    return wrap


def message_handler(update: Update, context: CallbackContext, message: str):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message)
