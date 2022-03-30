from datetime import datetime
import pygsheets
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
from telegram.ext import CallbackContext
from telegram.error import TelegramError
from telegram.parsemode import ParseMode

import database
import google_sheets
import logger
import settings
from models import UserAccount, UsersMatch, UsersMeeting, BotTask
from utils import format_message


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

                notification = session.query(BotTask).filter(
                    BotTask.bot_task_type == 'form_accepted').first()
                if notification:
                    context.bot.send_message(
                        chat_id=user_db_record.user_id, text=format_message(
                            notification, db_user=user_db_record),
                        parse_mode=ParseMode.MARKDOWN)
            except IntegrityError:
                logger.logger.error('Cant save form info to db for user {}({})'.format(
                    user_db_record.user_name, user_db_record.user_id))
                session.rollback()
        else:
            logger.logger.error(
                'Cant process form, user {} not registered by bot'.format(user[3]))
            continue

        logger.logger.info('User {}({}) form registered'.format(
            user_db_record.user_name, user_db_record.user_id))


def send_matchs(context: CallbackContext):
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

        notification = session.query(BotTask).filter(
            BotTask.bot_task_type == 'match_message').first()

        try:
            if notification:
                context.bot.send_message(
                    chat_id=match.user2_id, text=format_message(
                        notification, db_user=match.user1),
                    parse_mode=ParseMode.MARKDOWN)
                meeting.user_1_delivered = True
        except TelegramError as err:
            logger.logger.error('Could not deliver meeting {}, for user 1 {}: {}'.format(
                meeting.meeting_id, match.user1_id, err.message))

        try:
            context.bot.send_message(
                chat_id=match.user1_id, text=format_message(
                    notification, db_user=match.user2),
                parse_mode=ParseMode.MARKDOWN)
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
