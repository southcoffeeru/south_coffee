from asyncio.log import logger
import logging

import settings


def init():
    global logger

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.getLevelName(settings.CONFIG['log_level'].upper()))
