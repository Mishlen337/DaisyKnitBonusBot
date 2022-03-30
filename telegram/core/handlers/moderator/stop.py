from aiogram import types
from aiogram.dispatcher.storage import FSMContext


async def stop_handler(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Стейт сброшен!")
