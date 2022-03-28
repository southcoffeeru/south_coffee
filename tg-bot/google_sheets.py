import pygsheets

import settings


def init():
    global google_sheets
    google_sheets = pygsheets.authorize(
        service_account_file=settings.CONFIG['google_sheets_token_path'])
