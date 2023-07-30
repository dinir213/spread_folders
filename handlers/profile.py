from aiogram import types, Dispatcher
from create_bot import bot, dp

@dp.callback_query_handler(text=["profile"])
async def see_profile(call: types.CallbackQuery):
