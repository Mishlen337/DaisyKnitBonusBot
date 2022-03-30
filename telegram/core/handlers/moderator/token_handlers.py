from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loguru import logger
from core.database.repositories.user import UserRepository
from core.database.create_table import SessionLocal
from core.database.repositories.token import TokenRepository


async def token_command_handler(message: types.Message, state: FSMContext):
    logger.debug(f"In token_command_handler - moderator {message.from_user}")
    await message.answer("Введите токен:")
    await state.set_data({"previous_state": (await state.get_state())})
    await state.set_state("token")


async def token_handler(message: types.Message, state: FSMContext):
    personal_token = message.text
    logger.debug(f"In token_handler - moderator {message.from_user} - token {personal_token}")
    logger.debug(f"Getting data from db")
    session = SessionLocal()
    logger.debug(f"Getting token from db for moderator {message.from_user}")
    tr = TokenRepository(session)
    db_token = await tr.get_one()
    logger.debug(f"Token got from db successfully {db_token}")
    try:
        if db_token["token"] == personal_token:
            logger.debug(f"Token valid")
            logger.debug(f"Setting moderator in db for user - {message.from_user}")
            ur = UserRepository(session)
            await ur.update(tg_chat_id=message.from_user.id, new_is_admin=True)
            logger.debug(f"Moderator set in db for user - {message.from_user}")
            await message.answer("Вы стали модератором!")
        else:
            await message.answer("Неверный токен :(")
    except:
        logger.debug(f"No token in data base")
    await state.set_state((await state.get_data())["previous_state"])
    await state.reset_data()
    await session.close()
