from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

inline_btn_1_menu = InlineKeyboardButton('Купить', callback_data='buy')
inline_btn_2_menu = InlineKeyboardButton('Профиль', callback_data='profile')
inline_btn_3_menu = InlineKeyboardButton('FAQ', callback_data='faq')
inline_btn_4_menu = InlineKeyboardButton('Саппорт', callback_data='support')
inline_btn_5_menu = InlineKeyboardButton('Пополнить баланс', callback_data='add_balance')
inline_btn_6_menu = InlineKeyboardButton('Меню администратора', callback_data='admins')
inline_kb_menu = InlineKeyboardMarkup()\
    .row(inline_btn_1_menu, inline_btn_2_menu)\
    .row(inline_btn_3_menu, inline_btn_4_menu)\
    .add(inline_btn_5_menu)\
    .add(inline_btn_6_menu)

back_btn = InlineKeyboardButton('Назад', callback_data='back')
inline_kb_back_in_menu = InlineKeyboardMarkup().add(back_btn)

async def print_all_categories(all_categories, code_data_base):
    inline_kb_all_categories = InlineKeyboardMarkup()
    flag = 0
    if all_categories != []:
        flag = 1
        for category in all_categories:
            inline_kb_all_categories.add(types.InlineKeyboardButton(text=category[0], callback_data=f'select~{category[0]}~{code_data_base}'))
    return [inline_kb_all_categories.add(back_btn), flag]