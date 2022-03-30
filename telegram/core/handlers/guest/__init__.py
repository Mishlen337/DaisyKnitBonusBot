from aiogram import Dispatcher

from .email_handler import email_handler as e_handler
from .photo_handlers import photo_handler, phone_handler, error_photo_handler


def setup(dp: Dispatcher):
    """Function for recusivevly register dispatchers"""
    dp.register_message_handler(e_handler, state="email")
    dp.register_message_handler(photo_handler, state="photo", content_types=["photo"])
    dp.register_message_handler(error_photo_handler, state="photo")
    dp.register_message_handler(phone_handler, state="phone")
