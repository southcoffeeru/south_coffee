from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import Updater, Dispatcher

import database
import logger
import settings
from handlers import start, echo, caps


def main():
    settings.init()
    database.init()
    logger.init()
    updater = Updater(token=settings    .CONFIG['api_token'], use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
