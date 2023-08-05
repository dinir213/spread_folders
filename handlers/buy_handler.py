from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from keyboards.num_buttons import kb_num_buttons
from keyboards.menu_kb import print_all_categories, inline_kb_back_in_menu
from data_base.admin_db import view_all_subcategories_db, get_info_about_tov
from data_base.tov_or_paym_menu_db import input_tov_menu_info
from create_bot import bot
class select_tov(StatesGroup):
    category = State()
    subcategory = State()
async def select_subcatecory(call: types.CallbackQuery, state: FSMContext):
    text = call.data.split('₢')
    if text[2] == 'category':
        select_category = text[1]
        subcategory_menu = await print_all_categories(await view_all_subcategories_db(select_category), 'subcategory')
        if subcategory_menu[1] == 0:
            await call.message.edit_text(f'Товаров в данной категории пока нет', reply_markup=subcategory_menu[0])
        else:
            await call.message.edit_text(f'Выберите товар:', reply_markup=subcategory_menu[0])
        await input_tov_menu_info(call, select_category, text[2])
    elif text[2] == 'subcategory':
        select_subcategory = text[1]
        select_category = await input_tov_menu_info(call, select_subcategory, text[2])
        info_tov = await get_info_about_tov(select_category, select_subcategory)
        photo = InputFile(f"imgs/{info_tov[4]}.jpg")
        inline_kb_num_buttons = await kb_num_buttons("tov_add_")
        await call.message.delete()
        await bot.send_photo(photo=photo, chat_id=call.message.chat.id, caption=f"<b>💎 Категория:</b> <i>{select_category}</i>\n<b>💎 Подкатегория:</b> <i>{select_subcategory}</i>\n<b>💰 Цена:</b> <i>{info_tov[2]} руб</i>\n<b>📀 На складе:</b> <i>{info_tov[1]} шт.</i>\n<b>💚 Описание:</b> <i>{info_tov[3]}</i>", parse_mode='html', reply_markup=inline_kb_num_buttons)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(select_subcatecory, text_startswith=["select₢"], state="*")