from keyboards import admin_kb
from aiogram import types, Dispatcher
async def menu_admin(call: types.CallbackQuery):
    await call.message.edit_caption(f"Меню Администратора\n\nВыберите:", reply_markup=admin_kb.inline_kb_admin)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(menu_admin, text=["admins"])
