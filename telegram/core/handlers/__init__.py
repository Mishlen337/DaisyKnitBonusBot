from aiogram import Dispatcher
from loguru import logger

from . import guest, moderator

from .start_handler import start_handler as s_handler


def setup(dp: Dispatcher):
    """Function for recursivly register dispatchers

    Args:
        dp (Dispatcher)
    """
    logger.debug("Start base handler dispatcher")
    moderator.setup(dp)
    guest.setup(dp)
    dp.register_message_handler(s_handler, commands="start")
    logger.debug("End base handler dispatcher")
