from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

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
    types.InlineKeyboardButton(text='CLEAR', callback_data='deposit:clear'),
    types.InlineKeyboardButton(text='Оплата картой ☑️', callback_data='getcheck'),
    types.InlineKeyboardButton(text='Оплата криптой ☑️', callback_data='getcheck_crypto')).add(InlineKeyboardButton(text='Назад', callback_data='back_in_menu'))