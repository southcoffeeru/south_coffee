import datetime

from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import Updater, Dispatcher

import database
import google_sheets
import logger
import settings

from handlers import start, create_match
from jobs import parse_new_forms, send_matchs


def main():
    settings.init()
    database.init()
    google_sheets.init()
    logger.init()

    updater = Updater(token=settings.CONFIG['tg_api_token'], use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    delta = datetime.timedelta(seconds=15)
    dispatcher.job_queue.run_repeating(
        parse_new_forms, delta, name='parse_new_forms')
    dispatcher.job_queue.run_repeating(
        send_matchs, delta, name='send_matchs')

    create_match_handler = CommandHandler('create_match', create_match)
    dispatcher.add_handler(create_match_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
