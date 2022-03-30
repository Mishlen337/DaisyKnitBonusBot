import re
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loguru import logger
from core.database.repositories.user import UserRepository
from core.database.create_table import SessionLocal
# from core.utils import google


async def error_photo_handler(message: types.Message, state: FSMContext):
    logger.debug(f"In error photo handler - guest {message.from_user}")
    await message.answer("Пришлите фото опубликованного отзыва на WILDBERRIES:")


async def photo_handler(message: types.Message, state: FSMContext):
    logger.debug(f"In photo handler - guest {message.from_user}")
    message_id = message.message_id
    logger.debug(f"Setting message_id in state storage - guest {message.from_user}")
    await state.set_data({"message_id": message_id})
    await message.answer("Номер телефона, на который удобно получить бонус:")
    await state.set_state("phone")


async def phone_handler(message: types.Message, state: FSMContext):
    phone = message.text
    logger.debug(f"In phone handler - guest {message.from_user}, phone - {phone}")
    if re.findall(
        r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
        phone,
    ):
        logger.debug(f"Getting data from db")
        session = SessionLocal()
        ur = UserRepository(session)
        logger.debug(f"Getting admins from db")
        admin_list = await ur.get_all(is_admin=True)
        logger.debug(f"Admins got successfully {admin_list}")
        logger.debug(f"Getting user from db")
        user = await ur.get_one(tg_chat_id=message.from_user.id)
        logger.debug(f"User - {user} got from db successfully")
        await session.close()
        try:
            message_id = (await state.get_data())["message_id"]
            logger.debug(f"Forwading message with photoes to admins - guest {message.from_user}")
            for admin in admin_list:
                await message.bot.send_chat_action(admin["tg_chat_id"], types.ChatActions.TYPING)
                await message.bot.send_message(
                    admin["tg_chat_id"],
                    f"Пользователь - email: {user['email']}; номер телефона: {phone}; ник в телеграмме: @{message.from_user.username};",
                )
                await message.bot.forward_message(
                    admin["tg_chat_id"], message.from_user.id, message_id
                )
        except:
            logger.debug(f"No previous data in storage")

        values = [[user["email"], phone]]
        # google.append_row(values)
        await state.reset_data()
        await state.set_state("photo")
        await message.answer("🎁До новых встреч, Ваша команда DAISYKNIT!")
    else:
        await message.answer(
            "Уф.. 😞 Не могу разобрать твой телефон, пожалуйста, пришли свой телефон в формате `8(999)999-99-99`."
        )
