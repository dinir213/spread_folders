from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import menu_kb
from keyboards.num_buttons import kb_num_buttons
from data_base.tov_or_paym_menu_db import create_tov_menu_info
from data_base import profile_db, tov_or_paym_menu_db, admin_db
from create_bot import bot

import asyncio
from aiogram.types import InputFile

async def menu_profile(call: types.CallbackQuery):
    profile_data = await profile_db.get_profile(call.from_user.id)
    if profile_data[4] == '':
        count_referals = 0
    else:
        count_referals = len((profile_data[4]).split(","))
    print(profile_data)
    await call.message.edit_caption(f'Ваш профиль:\n\nЮзер: @{call.from_user.username}\nID: {call.from_user.id}\nБаланс: {profile_data[2]} руб\nКоличество приглашенных: {count_referals}\n\nРеферальная ссылка:\nhttps://t.me/Openheimer_bot?start={call.from_user.id}', reply_markup=menu_kb.inline_kb_back_in_menu)
async def menu_faq(call: types.CallbackQuery):
    await call.message.edit_caption(f"По различным вопросам обращайтесь к @gilmanovdin", reply_markup=menu_kb.inline_kb_back_in_menu)
    # nw_photo = 'https://blog.eldorado.ru/storage/publication/MWk3qOYojw6LEZDFtaDhWDTTrflixkdASgBDoR4T.jpeg'
    photo_url = 'imgs/YDYGUEVSZ7U4.jpg'
    with open(photo_url, 'rb') as photo_file:
        new_photo = types.InputMediaPhoto(media=photo_file)
        await bot.edit_message_media(media=new_photo, chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption='По различным вопросам обращайтесь к @victor_buterin', reply_markup=menu_kb.inline_kb_back_in_menu)

async def menu_support(call: types.CallbackQuery):
    await call.message.edit_caption(f"По различным вопросам обращайтесь к @victor_buterin", reply_markup=menu_kb.inline_kb_back_in_menu)

async def menu_add_balance(call: types.CallbackQuery):
    await call.message.edit_caption(f"Для пополнения счета введите суммы, которую хотите пополнить:", reply_markup=(await kb_num_buttons('deposit')))
    await tov_or_paym_menu_db.input_value_amount_in_menu_payment(call)
async def menu_buy_main(call: types.CallbackQuery):
    category_menu = await menu_kb.print_all_categories(await admin_db.view_all_categories_db(), 'category')
    print(f"Ошибочная клавиатура при покупке: {category_menu}")

    if category_menu[1] == 1:
        await call.message.edit_caption(f'Выберите категорию товаров:', reply_markup=category_menu[0])
        await create_tov_menu_info(call)
    elif category_menu[1] == 0:
        await call.message.edit_caption(f'Категории пока не добавлены', reply_markup=category_menu[0])


async def back_in_menu(call: types.CallbackQuery, state=FSMContext):
    if await state.get_data() != None:
        await state.finish()
    try:
        await call.message.edit_caption(f'Добро пожаловать, {call.from_user.first_name}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
    except:
        await call.message.delete()

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(menu_profile, text=["profile"])
    dp.register_callback_query_handler(menu_faq, text=["faq"])
    dp.register_callback_query_handler(menu_support, text=["support"])
    dp.register_callback_query_handler(menu_add_balance, text=["add_balance"])
    dp.register_callback_query_handler(menu_buy_main, text=["buy"])
    dp.register_callback_query_handler(back_in_menu, text=["back"], state="*")
