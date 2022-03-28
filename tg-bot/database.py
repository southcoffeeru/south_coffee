from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import settings


def init():
    global db
    db = create_engine(settings.CONFIG['db_connection_string'])


def session():
    return Session(bind=db)
