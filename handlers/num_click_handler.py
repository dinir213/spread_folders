from aiogram import types, Dispatcher
from data_base import tov_or_paym_menu_db
from keyboards.num_buttons import kb_num_buttons, inline_kb_confirm_buy
from create_bot import bot
from data_base.admin_db import get_info_about_tov
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
class info_tovs(StatesGroup):
    count_tovs = State()
async def click_handler(call: types.CallbackQuery, state: FSMContext):
    text = call.data.split(":")
    print(text)
    flag = text[0]
    btn = text[1]
    if flag == 'deposit':
        flag = False
        if btn != 'clear':
            last_value = await tov_or_paym_menu_db.get_value_amount_in_menu_payment(call)
            if last_value != '' or (btn != '.' and int(btn) != 0):
                btn = f'{last_value}{btn}'
                flag = True
        if not flag:
            btn = ''
        await bot.answer_callback_query(call.id)
        try:
            await call.message.edit_text(f'Для пополнения счета введите суммы, которую хотите пополнить: {btn} руб', reply_markup=(await kb_num_buttons('deposit')))
        except:
            pass
        await tov_or_paym_menu_db.update_value_amount_in_menu_payment(call, btn)
    elif flag == 'tov_add_':
        tov_menu_info = await tov_or_paym_menu_db.get_count_tov_menu_info(call)
        flag = False
        if btn != 'clear':
            last_value = tov_menu_info[4]
            if last_value != '' or (btn != '.' and int(btn) != 0):
                btn = f'{last_value}{btn}'
                flag = True
        if not flag:
            btn = ''
        inline_kb_num_buttons = await kb_num_buttons("tov_add_")
        select_category = tov_menu_info[2]
        select_subcategory = tov_menu_info[3]
        await tov_or_paym_menu_db.update_count_tov_menu_info(call, btn)
        if btn == '':
            btn = 0
        info_tov = await get_info_about_tov(select_category, select_subcategory)
        await call.message.edit_caption(
            caption=f"<b>💎 Категория:</b> <i>{select_category}</i>\n<b>💎 Подкатегория:</b> <i>{select_subcategory}</i>\n<b>💰 Цена:</b> <i>{info_tov[2]} руб</i>\n<b>📀 На складе:</b> <i>{info_tov[1]} шт.</i>\n<b>💚 Описание:</b> <i>{info_tov[3]}</i>\n\n\n➖ПОКУПКА➖\nКоличество: {btn}\nСумма к списанию: {float(btn) * info_tov[2]}\n➖",
            parse_mode='html', reply_markup=inline_kb_num_buttons)
        await bot.answer_callback_query(call.id)
    elif flag == 'view_confirm':
        tov_menu_info = await tov_or_paym_menu_db.get_count_tov_menu_info(call)
        select_category = tov_menu_info[2]
        select_subcategory = tov_menu_info[3]
        info_tov = await get_info_about_tov(select_category, select_subcategory)
        await call.message.edit_caption(caption=f"<b>💎 Категория:</b> <i>{select_category}</i>\n<b>💎 Подкатегория:</b> <i>{select_subcategory}</i>\n<b>💰 Цена:</b> <i>{info_tov[2]} руб</i>\n<b>📀 На складе:</b> <i>{info_tov[1]} шт.</i>\n<b>💚 Описание:</b> <i>{info_tov[3]}</i>\n\n\n➖ПОКУПКА➖\nКоличество: {btn}\nСумма к списанию: {float(tov_menu_info[4]) * info_tov[2]}\n➖",parse_mode='html', reply_markup=inline_kb_confirm_buy)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(click_handler, text_startswith=["deposit:", "tov_add_", "view_confirm"], state="*")
