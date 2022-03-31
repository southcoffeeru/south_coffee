import string

from telegram import User
from telegram.ext import CallbackContext
from models import BotTask, UserAccount
from telegram.parsemode import ParseMode

import database
import logger


def format_message(task: BotTask, tg_user: User = None, db_user: UserAccount = None):
    def replace_macro(markup: str, tg_user: User, db_user: UserAccount) -> str:
        class BlankFormatter(string.Formatter):
            def __init__(self, default=''):
                self.default = default

            def get_value(self, key, args, kwds):
                if isinstance(key, str):
                    return kwds.get(key, self.default)
                else:
                    return string.Formatter.get_value(key, args, kwds)

        fmt = BlankFormatter()
        macroses = {}
        if tg_user:
            macroses.update({
                'TG_USER_FIRST_NAME':   tg_user.first_name,
                'TG_USER_LAST_NAME':    tg_user.last_name,
                'TG_USER_FULL_NAME':    tg_user.full_name,
            })

        if db_user:
            macroses.update({
                'DB_USER_NICKNAME': db_user.user_tg_nickname,
                'DB_USER_NAME': db_user.user_name,
                'DB_USER_TYPE_OF_ACTIVITY': db_user.user_type_of_activity,
                'DB_USER_INTERESTS': db_user.user_interests,
                'DB_USER_ATTRACTIVNESS': db_user.user_attractiveness,
                'DB_USER_CITY': db_user.user_city,
                'DB_USER_EMAIL': db_user.user_email
            })
        return fmt.format(markup, **macroses)

    title = '*{}*  \n'.format(replace_macro(task.bot_task_title,
                              tg_user=tg_user, db_user=db_user))
    content = replace_macro(task.bot_task_content,
                            tg_user=tg_user, db_user=db_user)
    return '{}{}'.format(title, content)


def send_formated_message(context: CallbackContext, chat_id: int, task_type: str, **kwargs):
    session = database.session()
    task: BotTask = session.query(BotTask).filter(
        BotTask.bot_task_type == task_type).first()

    if task:
        context.bot.send_message(
            chat_id=chat_id, text=format_message(
                task, **kwargs),
            parse_mode=ParseMode.MARKDOWN)
    else:
        logger.logger.error(
            'No {} messages found in bot tasks'.format(task_type))
