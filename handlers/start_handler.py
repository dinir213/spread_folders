from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import menu_kb
from data_base import profile_db
from data_base.tov_or_paym_menu_db import del_tov_menu_info


async def command_start(message: types.Message):
    args = message.get_args() # /start 123123
    referer = await profile_db.check_args(args, message.from_user.id)
    await bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}! Спасибо, что выбрали наш магазин!\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
    await message.delete()
    await profile_db.create_profile(message, referer)
async def command_start_call(call: types.CallbackQuery):
    await del_tov_menu_info(call)
    await call.message.delete()
    await bot.send_message(call.from_user.id, f'Добро пожаловать, {call.from_user.first_name}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_callback_query_handler(command_start_call, text=['start'])

