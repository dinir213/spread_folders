from aiogram.types import CallbackQuery
from data_base.profile_db import get_count_all_users
from keyboards.menu_kb import inline_kb_back_in_menu
from aiogram import Dispatcher
async def view_statistic(call: CallbackQuery):
    count_all_users = await get_count_all_users()
    await call.message.edit_caption(f'Статистика:\n\nОбщее кол-во юзеров: {count_all_users}', reply_markup=inline_kb_back_in_menu)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(view_statistic, text=["statistic"])