import string

from telegram import User
from models import BotTask


def format_message(task: BotTask, user: User):
    def replace_macro(markup: str, user: User) -> str:
        class BlankFormatter(string.Formatter):
            def __init__(self, default=''):
                self.default = default

            def get_value(self, key, args, kwds):
                if isinstance(key, str):
                    return kwds.get(key, self.default)
                else:
                    return string.Formatter.get_value(key, args, kwds)

        fmt = BlankFormatter()
        return fmt.format(markup,
                          FIRST_NAME=user.first_name,
                          LAST_NAME=user.last_name,
                          FULL_NAME=user.full_name
                          )

    title = '*{}*  \n'.format(replace_macro(task.bot_task_title, user))
    content = replace_macro(task.bot_task_content, user)
    return '{}{}'.format(title, content)
