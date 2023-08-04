from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot, storage
from keyboards import menu_kb, num_buttons
from keyboards.num_buttons import kb_num_buttons
from data_base.tov_or_paym_menu_db import create_tov_menu_info
from data_base import start_db, profile_db, tov_or_paym_menu_db, admin_db
async def menu_profile(call: types.CallbackQuery):
    profile_data = await profile_db.get_profile(call.from_user.id)
    await call.message.edit_text(f'Ваш профиль:\n\nЮзер: @{call.from_user.username}\nID: {call.from_user.id}\nБаланс: {profile_data[2]} руб', reply_markup=menu_kb.inline_kb_back_in_menu)
async def menu_faq(call: types.CallbackQuery):
    await call.message.edit_text(f"По различным вопросам обращайтесь к @gilmanovdin", reply_markup=menu_kb.inline_kb_back_in_menu)
async def menu_support(call: types.CallbackQuery):
    await call.message.edit_text(f"По различным вопросам обращайтесь к @gilmanovdin", reply_markup=menu_kb.inline_kb_back_in_menu)

async def menu_add_balance(call: types.CallbackQuery):
    await call.message.edit_text(f"Для пополнения счета введите суммы, которую хотите пополнить:", reply_markup=(await kb_num_buttons()))
    await tov_or_paym_menu_db.input_value_amount_in_menu_payment(call)
async def menu_buy_main(call: types.CallbackQuery):
    category_menu = await menu_kb.print_all_categories(await admin_db.view_all_categories_db(), 'category')
    print(category_menu[0])
    await create_tov_menu_info(call)
    await call.message.edit_text(f'Выберите категорию товаров:', reply_markup=category_menu[0])

async def back_in_menu(call: types.CallbackQuery, state=FSMContext):
    if await state.get_data() != None:
        await state.finish()
    await call.message.edit_text(f'Добро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(menu_profile, text=["profile"])
    dp.register_callback_query_handler(menu_faq, text=["faq"])
    dp.register_callback_query_handler(menu_support, text=["support"])
    dp.register_callback_query_handler(menu_add_balance, text=["add_balance"])
    dp.register_callback_query_handler(menu_buy_main, text=["buy"])
    dp.register_callback_query_handler(back_in_menu, text=["back"], state="*")
