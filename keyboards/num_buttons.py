from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from data_base.admin_db import view_all_payment_methods
async def kb_num_buttons():
    inline_kb_num_buttons = InlineKeyboardMarkup(row_width=3).add(
        types.InlineKeyboardButton(text='1', callback_data='deposit:1'),
        types.InlineKeyboardButton(text='2', callback_data='deposit:2'),
        types.InlineKeyboardButton(text='3', callback_data='deposit:3'),
        types.InlineKeyboardButton(text='4', callback_data='deposit:4'),
        types.InlineKeyboardButton(text='5', callback_data='deposit:5'),
        types.InlineKeyboardButton(text='6', callback_data='deposit:6'),
        types.InlineKeyboardButton(text='7', callback_data='deposit:7'),
        types.InlineKeyboardButton(text='8', callback_data='deposit:8'),
        types.InlineKeyboardButton(text='9', callback_data='deposit:9'),
        types.InlineKeyboardButton(text='.', callback_data='deposit:.'),
        types.InlineKeyboardButton(text='0', callback_data='deposit:0'),
        types.InlineKeyboardButton(text='CLEAR', callback_data='deposit:clear'))
    all_payment_methods = await view_all_payment_methods()
    for i in all_payment_methods:
        if i[2] == '1':
            print(f'{i[1]}')
            inline_kb_num_buttons.add(types.InlineKeyboardButton(text=f'Оплата через {i[0]} ☑', callback_data=f'{i[1]}'))
    return inline_kb_num_buttons.add(InlineKeyboardButton(text='Назад', callback_data='back'))

async def kb_check_payment_buttons(payment_method):
    return InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Подтвердить ✅', callback_data=f'successful.payment_{payment_method}'),
        types.InlineKeyboardButton(text='Отмена', callback_data='successful.payment_back')
    )