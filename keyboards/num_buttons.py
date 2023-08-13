from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from data_base.admin_db import view_all_payment_methods
async def kb_num_buttons(callback_info):
    inline_kb_num_buttons = InlineKeyboardMarkup(row_width=3).add(
        types.InlineKeyboardButton(text='1', callback_data=f'{callback_info}:1'),
        types.InlineKeyboardButton(text='2', callback_data=f'{callback_info}:2'),
        types.InlineKeyboardButton(text='3', callback_data=f'{callback_info}:3'),
        types.InlineKeyboardButton(text='4', callback_data=f'{callback_info}:4'),
        types.InlineKeyboardButton(text='5', callback_data=f'{callback_info}:5'),
        types.InlineKeyboardButton(text='6', callback_data=f'{callback_info}:6'),
        types.InlineKeyboardButton(text='7', callback_data=f'{callback_info}:7'),
        types.InlineKeyboardButton(text='8', callback_data=f'{callback_info}:8'),
        types.InlineKeyboardButton(text='9', callback_data=f'{callback_info}:9'))
    if callback_info == 'deposit':
        all_payment_methods = await view_all_payment_methods()
        inline_kb_num_buttons.add(
            types.InlineKeyboardButton(text='.', callback_data='deposit:.'),
            types.InlineKeyboardButton(text='0', callback_data='deposit:0'),
            types.InlineKeyboardButton(text='CLEAR', callback_data='deposit:clear'))
        for i in all_payment_methods:
            if i[2] == '1':
                inline_kb_num_buttons.add(types.InlineKeyboardButton(text=f'Оплата через {i[0]} ☑', callback_data=f'{i[1]}'))
        return inline_kb_num_buttons.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    elif callback_info == 'tov_add_':
        return inline_kb_num_buttons.add(
            types.InlineKeyboardButton(text='Назад', callback_data='start'),
            types.InlineKeyboardButton(text='0', callback_data='tov_add_:0'),
            types.InlineKeyboardButton(text='CLEAR', callback_data='tov_add_:clear')).add(types.InlineKeyboardButton(text='КУПИТЬ', callback_data='view_confirm:'))

inline_kb_confirm_buy = InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text='❎ Отмена', callback_data='confirm_cancel_buy'),
    types.InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm_accept_buy'))


async def kb_check_payment_buttons(payment_method):
    return InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Подтвердить ✅', callback_data=f'successful.payment_{payment_method}'),
        types.InlineKeyboardButton(text='Отмена', callback_data='successful.payment_back')
    )

