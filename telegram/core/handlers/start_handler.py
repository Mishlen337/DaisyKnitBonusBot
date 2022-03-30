from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loguru import logger
from core.database.repositories.user import UserRepository
from core.database.create_table import SessionLocal


async def start_handler(message: types.Message, state: FSMContext):
    logger.debug(f"In start handler - guest {message.from_user}")
    session = SessionLocal()
    ur = UserRepository(session)
    logger.debug(f"Adding guest {message.from_user.id} in db")
    try:
        await ur.add({"tg_chat_id": message.from_user.id})
        logger.debug(f"Guest {message.from_user.id} successfully added in db")
    except ValueError:
        logger.debug(f"Guest is already exist")
    await session.close()
    await message.answer(
        """Добрый день!🌺
Благодарим Вас за выбор нашей марки, носите с удовольствием и вдохновением! 
❤️
Рады будем отправить для Вас бонус 🎁
(200 рублей на счет/телефон), если 
оставите отзыв с фото о нашем изделии.
💌Пожалуйста, ответьте на несколько вопросов:"""
    )
    await message.answer("Ваш электронный адрес:")
    await state.set_state("email")
