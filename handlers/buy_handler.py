import time

from aiogram import types, Dispatcher
from aiogram.types import InputFile
from data_base.profile_db import edit_profile
from keyboards.num_buttons import kb_num_buttons, kb_confirm_buy_tov
from keyboards.menu_kb import print_all_categories, inline_kb_back_in_menu
from data_base.admin_db import view_all_subcategories_db, get_info_about_tov, sell_position_db, update_count_tovs_db
from data_base.profile_db import get_profile
from data_base.tov_or_paym_menu_db import input_tov_menu_info, get_count_tov_menu_info
from create_bot import bot

async def select_subcatecory(call: types.CallbackQuery):
    timestart = time.perf_counter()
    text = call.data.split('~')
    if text[2] == 'category':
        select_category = text[1]
        subcategory_menu = await print_all_categories(await view_all_subcategories_db(select_category), 'subcategory')
        if subcategory_menu[1] == 0:
            await call.message.edit_caption(f'Товаров в данной категории пока нет', reply_markup=subcategory_menu[0])
        else:
            await call.message.edit_caption(f'Выберите товар:', reply_markup=subcategory_menu[0])
        await input_tov_menu_info(call, select_category, text[2])
    elif text[2] == 'subcategory':
        select_subcategory = text[1]
        select_category = await input_tov_menu_info(call, select_subcategory, text[2])
        info_tov = await get_info_about_tov(select_category, select_subcategory)
        photo = InputFile(f"imgs/{info_tov[4]}.jpg")
        inline_kb_num_buttons = await kb_num_buttons("tov_add_")
        # await call.message.delete()
        # await bot.send_photo(photo=photo, chat_id=call.message.chat.id)
        photo_url = f'imgs/{info_tov[4]}.jpg'
        with open(photo_url, 'rb') as photo_file:
            new_photo = types.InputMediaPhoto(media=photo_file)
            await bot.edit_message_media(media=new_photo, chat_id=call.message.chat.id,message_id=call.message.message_id)
            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,caption=f"💎 Категория: {select_category}\n💎 Подкатегория: {select_subcategory}\n💰 Цена: {info_tov[2]} руб\n📀 На складе: {info_tov[1]} шт.\n💚 Описание: {info_tov[3]}", reply_markup=inline_kb_num_buttons)

        # await bot.send_photo(photo=photo, chat_id=call.message.chat.id, caption=f"<b>💎 Категория:</b> <i>{select_category}</i>\n<b>💎 Подкатегория:</b> <i>{select_subcategory}</i>\n<b>💰 Цена:</b> <i>{info_tov[2]} руб</i>\n<b>📀 На складе:</b> <i>{info_tov[1]} шт.</i>\n<b>💚 Описание:</b> <i>{info_tov[3]}</i>", parse_mode='html', reply_markup=inline_kb_num_buttons)

    idle = time.perf_counter() - timestart
    print('accept buy func:', idle)
async def buy_tov_phase2(call: types.CallbackQuery):
    timestart = time.perf_counter()
    confirm = call.data.split("~")[1]
    if confirm == 'accept_buy':
        select_tov = await get_count_tov_menu_info(call)
        select_category = select_tov[2]
        select_subcategory = select_tov[3]
        info_tov = await get_info_about_tov(select_category, select_subcategory)
        balance = (await get_profile(call.from_user.id))[2]
        if int(select_tov[4]) > int(info_tov[1]):
            await call.answer('Недостаточно товаров на складе')
        elif balance >= info_tov[2] * float(select_tov[4]):
            logins_parols = await sell_position_db(select_subcategory, int(select_tov[4]))
            if len(logins_parols) > 1024:
                for x in range(0, len(logins_parols), 4095):
                    await call.message.answer(logins_parols[x:x + 4095])
            else:
                await call.message.edit_caption(f"Покупка успешно пройдена:\n\n{logins_parols}")
            await update_count_tovs_db(-1, 'subcategory', select_category, select_subcategory)
            await edit_profile(call, -(info_tov[2] * float(select_tov[4])))

        else:
            await call.answer('Недостаточно баланса на счета')
        idle = time.perf_counter() - timestart
        print('accept buy func:', idle)
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(select_subcatecory, text_startswith=["select~"], state="*")
    dp.register_callback_query_handler(buy_tov_phase2, text_startswith=["confirm~"])