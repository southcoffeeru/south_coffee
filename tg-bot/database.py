from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import settings
import logger


def init():
    global db
    db = create_engine(settings.CONFIG['db']['connection_string'],
                       pool_size=settings.CONFIG['db']['query_pool_size'])


def session() -> Session:
    session = Session(bind=db)
    logger.logger.debug(
        'Acquire new session, Engine status: {}'.format(db.pool.status()))
    return session
