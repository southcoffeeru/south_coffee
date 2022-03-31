from datetime import datetime

import pygsheets
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
from telegram import Update, User
from telegram.error import TelegramError
from telegram.ext import CallbackContext

import database
import google_sheets
import logger
import settings
from models import UserAccount, UsersMatch, UsersMeeting
from utils import send_formated_message


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

            is_filled_first_time = False
            if not user_db_record.form_filled_at:
                user_db_record.form_filled_at = ts
                is_filled_first_time = True
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
                send_formated_message(context, user_db_record.user_id,
                                      'form_accepted' if is_filled_first_time else 'form_updated', db_user=user_db_record)
            except IntegrityError:
                logger.logger.error('Cant save form info to db for user {}({})'.format(
                    user_db_record.user_name, user_db_record.user_id))
                session.rollback()
        else:
            logger.logger.debug(
                'Cant process form, user {} not registered by bot'.format(user[3]))
            continue

        logger.logger.info('User {}({}) form registered'.format(
            user_db_record.user_name, user_db_record.user_id))


def send_new_matches(context: CallbackContext):
    session = database.session()
    matchs_to_send = session.query(UsersMatch).filter(
        ~ exists().where(UsersMatch.match_id == UsersMeeting.match_id)).all()

    match: UsersMatch
    for match in matchs_to_send:
        try:
            meeting = UsersMeeting(match_id=match.match_id)
            session.add(meeting)
            session.commit()
            logger.logger.info(
                'Meeting for match {} created successfully'.format(match.match_id))
        except:
            logger.logger.error(
                'Could not create meeting for match {}'.format(match.match_id))
            session.rollback()
            return

        try:
            send_formated_message(context, match.user2_id,
                                  'match_message', db_user=match.user1)
            meeting.user_1_delivered = True
        except TelegramError as err:
            logger.logger.error('Could not deliver meeting {}, for user 1 {}: {}'.format(
                meeting.meeting_id, match.user1_id, err.message))

        try:
            send_formated_message(context, match.user1_id,
                                  'match_message', db_user=match.user2)
            meeting.user_2_delivered = True
        except TelegramError:
            logger.logger.error('Could not deliver meeting {}, for user 2 {}: {}'.format(
                meeting.meeting_id, match.user1_id, err.message))

        try:
            session.commit()
            logger.logger
        except:
            logger.logger.error('Could not updated delivery statuses for meeting id {} -- user 1 status {}, user 1 status {}'.format(
                meeting.meeting_id, meeting.user_1_delivered, meeting.user_2_delivered))
            session.rollback()
