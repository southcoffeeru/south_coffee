from datetime import datetime
import pygsheets
from sqlalchemy.exc import IntegrityError
from telegram.ext import CallbackContext

import database
import google_sheets
import logger
import settings
from models import UserAccount


def parse_new_forms(context: CallbackContext):
    def read_gs_timestamp(ts: str) -> datetime:
        return datetime.strptime(ts, '%d.%m.%Y %H:%M:%S')

    worksheet: pygsheets.Worksheet = google_sheets.google_sheets.open_by_key(
        settings.CONFIG['google_sheet_id'])[0]

    session = database.session()
    user_row: dict
    for user_row in worksheet.get_all_records():
        user = list(user_row.values())
        ts = read_gs_timestamp(user[0])
        user_db_record: UserAccount = session.query(
            UserAccount).filter(UserAccount.user_tg_nickname == user[3]).first()
        if user_db_record:
            if user_db_record.form_updated_at and user_db_record.form_updated_at >= ts:
                logger.logger.debug('Google sheet record with ts {} for user {}({}) is outdated'.format(
                    ts, user_db_record.user_name, user_db_record.user_id))
                continue

            if not user_db_record.form_filled_at:
                user_db_record.form_filled_at = ts
            user_db_record.form_updated_at = ts
            user_db_record.user_name = user[1]
            user_db_record.user_email = user[2]
            user_db_record.user_type_of_activity = user[4]
            user_db_record.user_interests = user[5]
            user_db_record.user_attractiveness = user[6]
            user_db_record.user_others = user[7]
            user_db_record.user_city = user[8]
            try:
                session.commit()
            except IntegrityError:
                logger.logger.error('Cant save form info to db for user {}({})'.format(
                    user_db_record.user_name, user_db_record.user_id))
            finally:
                session.rollback()
        else:
            logger.logger.error(
                'Cant process form, user {} not registered by bot'.format(user[3]))
            continue

        logger.logger.info('User {}({}) form registered'.format(
            user_db_record.user_name, user_db_record.user_id))
