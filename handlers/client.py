from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot, storage
from keyboards import menu_kb
from data_base import start_db, profile_db
# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=open("imgs/photo1.jpg", "rb"), caption=f'Добро пожаловать @{message.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
    await message.delete()
    await profile_db.create_profile(message)

# @dp.callback_query_handler(text=["profile"])
async def menu_profile(call: types.CallbackQuery):
    profile_data = await profile_db.get_profile(str(call.from_user.id))
    await call.message.edit_caption(f'Ваш профиль:\n\nЮзер: {call.from_user.username}\nID: {call.from_user.id}\nБаланс: {profile_data[2]} руб', reply_markup=menu_kb.inline_kb_back_in_menu)

async def back_in_menu(call: types.CallbackQuery, state=FSMContext):
    if await state.get_data() != None:
        await state.finish()
    await call.message.edit_caption(f'Добро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_callback_query_handler(menu_profile, text=["profile"])
    dp.register_callback_query_handler(back_in_menu, text=["back"], state="*")
