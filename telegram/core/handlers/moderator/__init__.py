from aiogram import Dispatcher
from .stop import stop_handler
from .token_handlers import token_command_handler, token_handler


def setup(dp: Dispatcher):
    """Function for recusivevly register dispatchers"""
    dp.register_message_handler(stop_handler, commands="stop", state="*")
    dp.register_message_handler(token_command_handler, commands="token", state="*")
    dp.register_message_handler(token_handler, state="token")
