from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base.admin_db import view_all_payment_methods
from aiogram import types
# Клавиатура для админ-панели:
inline_btn_1_admin = InlineKeyboardButton('Способы оплаты', callback_data='add_payment_methods')
inline_btn_2_admin = InlineKeyboardButton('Добавить товар', callback_data='add_del_tov')
inline_btn_3_admin = InlineKeyboardButton('Процент за приглашение', callback_data='update_percent_referral')
inline_btn_4_admin = InlineKeyboardButton('Технические работы', callback_data='update_work_mode')
inline_btn_5_admin = InlineKeyboardButton('Рассылка', callback_data='mailing')

back_btn = InlineKeyboardButton('Назад', callback_data='back')
inline_kb_admin = InlineKeyboardMarkup().add(inline_btn_1_admin).add(inline_btn_2_admin).add(inline_btn_3_admin).add(inline_btn_4_admin).add(inline_btn_5_admin).add(back_btn)

# Клавиатура со способами оплаты:
async def create_kb_payment_methods():
    all_payment_methods = await view_all_payment_methods()
    inline_kb_add_payment_methods = InlineKeyboardMarkup()
    for i in all_payment_methods:
        if i[2] == '0':
            description_btn = f'❌ {i[0]} Выключен'
        else:
            description_btn = f'✅ {i[0]} Включен'
        inline_kb_add_payment_methods.add(types.InlineKeyboardButton(text=description_btn, callback_data=f'turn_paym_method:{i[0]}:{i[2]}'))
    return inline_kb_add_payment_methods.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))

# Клавиатура для выбора способа добавления категории товаров, подкатегории товара или позиции
inline_btn_add_del_tov_back = types.InlineKeyboardButton(text='Вернуться назад', callback_data='add_del_tov')
inline_kb_add_del_tov_back = InlineKeyboardMarkup().add(inline_btn_add_del_tov_back)


inline_btn_1_add_tov = InlineKeyboardButton('Добавить категорию', callback_data='btn_add_category')
inline_btn_2_add_tov = InlineKeyboardButton('Добавить подкатегорию', callback_data='btn_add_subcategory')
inline_btn_3_add_tov = InlineKeyboardButton('Добавить позицию', callback_data='btn_add_position')
inline_btn_1_del_tov = InlineKeyboardButton('Удалить категорию', callback_data='btn_del_category')
inline_btn_2_del_tov = InlineKeyboardButton('Удалить подкатегорию', callback_data='btn_del_subcategory')
inline_btn_3_del_tov = InlineKeyboardButton('Удалить позицию', callback_data='btn_del_position')
back_btn = InlineKeyboardButton('Назад', callback_data='back')
inline_kb_add_del_tov = InlineKeyboardMarkup()\
    .row(inline_btn_1_add_tov, inline_btn_1_del_tov)\
    .row(inline_btn_2_add_tov, inline_btn_2_del_tov)\
    .row(inline_btn_3_add_tov, inline_btn_3_del_tov)\
    .add(back_btn)

async def print_all_categories(all_categories, code_data_base):
    inline_kb_all_categories = InlineKeyboardMarkup()
    flag = 0
    if all_categories != []:
        flag = 1
        for category in all_categories:
            inline_kb_all_categories.add(types.InlineKeyboardButton(text=category[0], callback_data=f'change~{category[0]}~{code_data_base}'))
    return [inline_kb_all_categories.add(inline_btn_add_del_tov_back), flag]
# Создание клавиатуры для включения/выключения бота во время технических работ
async def markup_work_mode(mode):
    markup = InlineKeyboardMarkup()
    if mode == 0:
        markup.add(types.InlineKeyboardButton(text="Включить 🔛",callback_data=f'click_update_work_mode'))
    if mode == 1:
        markup.add(types.InlineKeyboardButton(text="Выключить 📴",callback_data=f'click_update_work_mode'))
    return markup.add(back_btn)

# Рассылка. Создание клавиатуры для рассылки:
async def markup_mailing():
    return InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Просто текст', callback_data='mailing~text'),
        types.InlineKeyboardButton(text='Текст с картинкой', callback_data='mailing~photo_and_text'))\
        .add(back_btn)
async def markup_confirm_mailing():
    return InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Начать рассылку', callback_data='confirmmailing')
    ).add(InlineKeyboardButton('Отмена', callback_data='back'))