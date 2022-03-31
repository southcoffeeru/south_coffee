from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import settings


def init():
    global db
    db = create_engine(settings.CONFIG['db']['connection_string'],
                       pool_size=settings.CONFIG['db']['query_pool_size'])


def session():
    return Session(bind=db)
