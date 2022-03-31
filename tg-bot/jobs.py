from telegram.ext import CallbackContext

from handlers_utils import parse_new_forms, send_new_matches


def parse_new_forms_job(context: CallbackContext):
    parse_new_forms(context)


def send_matches_job(context: CallbackContext):
    send_new_matches(context)
