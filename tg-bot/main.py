import datetime

from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import Updater, Dispatcher

import database
import google_sheets
import logger
import settings

from handlers import start, create_match, parse_forms, send_all_matches
from jobs import parse_new_forms, send_matches_job


def main():
    settings.init()
    database.init()
    google_sheets.init()
    logger.init()

    updater = Updater(token=settings.CONFIG['tg_api_token'], use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    parse_forms_period = datetime.timedelta(
        seconds=settings.CONFIG['parse_new_forms_job_period_sec'])
    dispatcher.job_queue.run_repeating(
        parse_new_forms, parse_forms_period, name='parse_new_forms')
    send_matches_period = datetime.timedelta(
        seconds=settings.CONFIG['send_matches_job_period_sec'])
    dispatcher.job_queue.run_repeating(
        send_matches_job, send_matches_period, name='send_matches')

    create_match_handler = CommandHandler('create_match', create_match)
    dispatcher.add_handler(create_match_handler)
    create_match_handler = CommandHandler('parse_forms', parse_forms)
    dispatcher.add_handler(create_match_handler)
    create_match_handler = CommandHandler('send_all_matches', send_all_matches)
    dispatcher.add_handler(create_match_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
