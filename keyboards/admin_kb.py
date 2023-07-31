from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base.admin_db import view_all_payment_methods
from aiogram import types
# Клавиатура для админ-панели:
inline_btn_1_admin = InlineKeyboardButton('Способы оплаты', callback_data='add_payment_methods')
back_btn = InlineKeyboardButton('Назад', callback_data='back')
inline_kb_admin = InlineKeyboardMarkup().add(inline_btn_1_admin).add(back_btn)

# Клавиатура со способами оплаты:
async def create_kb_payment_methods():
    all_payment_methods = await view_all_payment_methods()
    inline_kb_add_payment_methods = InlineKeyboardMarkup()
    for i in all_payment_methods:
        print(i)
        if i[2] == '0':
            description_btn = f'❌ {i[0]} Выключен'
        else:
            description_btn = f'✅ {i[0]} Включен'
        inline_kb_add_payment_methods.add(types.InlineKeyboardButton(text=description_btn, callback_data=f'turn_paym_method:{i[0]}:{i[2]}'))
    return inline_kb_add_payment_methods.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))