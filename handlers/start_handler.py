from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot, storage
from keyboards import menu_kb
from data_base import start_db, profile_db
# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=open("imgs/photo1.jpg", "rb"))
    await bot.send_message(message.from_user.id, f'Добро пожаловать @{message.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
    await message.delete()
    await profile_db.create_profile(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
