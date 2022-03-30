import re
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loguru import logger
from core.database.repositories.user import UserRepository
from core.database.create_table import SessionLocal


async def email_handler(message: types.Message, state: FSMContext):
    email = message.text
    logger.debug(f"In email handler - guest {message.from_user}, email - {email}")
    if re.findall(r"([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}", email):
        session = SessionLocal()
        logger.debug(f"Adding email {email} for guest {message.from_user}")
        ur = UserRepository(session)
        await ur.update(tg_chat_id=message.from_user.id, new_email=email)
        await session.close()
        logger.debug(f"Email {email} for guest {message.from_user} added successfully")
        await message.answer("Фото опубликованного отзыва на WILDBERRIES:")
        await state.set_state("photo")
    else:
        logger.debug("Error email format")
        await message.answer(
            "Уф.. 😞 Не могу разобрать твою почту, пожалуйста, пришли свой электронный адрес в формате `inbox@mail.ru`."
        )
