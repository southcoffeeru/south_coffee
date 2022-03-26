from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import settings


def init():
    global session

    db = create_engine(settings.CONFIG['db_connection_string'])
    session = Session(bind=db)
