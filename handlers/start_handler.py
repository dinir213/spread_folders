from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot, storage
from keyboards import menu_kb
from data_base import start_db, profile_db
from data_base.tov_or_paym_menu_db import del_tov_menu_info
# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    # await bot.send_photo(message.from_user.id, photo=open("imgs/photo1.jpg", "rb"))
    await bot.send_message(message.from_user.id, f'Добро пожаловать @{message.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
    await message.delete()
    await profile_db.create_profile(message)
async def command_start_call(call: types.CallbackQuery):
    await del_tov_menu_info(call)
    await call.message.delete()
    await bot.send_message(call.from_user.id, f'Добро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
    # await message.delete()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_callback_query_handler(command_start_call, text=['start'])

