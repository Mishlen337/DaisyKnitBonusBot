from aiogram import Dispatcher
from loguru import logger

from . import guest, moderator


def setup(dp: Dispatcher):
    """Function for recursivly register dispatchers

    Args:
        dp (Dispatcher)
    """
    logger.debug("Start base handler dispatcher")
    guest.setup(dp)
    moderator.setup(dp)
    logger.debug("End base handler dispatcher")
