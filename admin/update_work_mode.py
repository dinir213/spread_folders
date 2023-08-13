from data_base.admin_db import get_work_mode_db, update_work_mode_db
from keyboards.admin_kb import markup_work_mode
from aiogram import Dispatcher, types
async def update_work_mode(call: types.CallbackQuery):
    work_mode = await get_work_mode_db()
    markup = await markup_work_mode(work_mode)
    await call.message.edit_text(f'Вы можете выключить бота для других пользователей, кроме Вас (чтобы выложить все товары, к примеру).\n\nЧтобы включить/выключить - нажмите на кнопку 👇', reply_markup=markup)
    # if work_mode == 1:
    #     await call.message.edit_text(f'Бот сейчас находится во включенном режиме. Чтобы выключить - нажмите на кнопку 👇', reply_markup=markup)
    # elif work_mode == 0:
    #     await call.message.edit_text(f'Бот сейчас находится в выключенном режиме. Чтобы включить - нажмите на кнопку 👇', reply_markup=markup)

async def update_work_mode_click(call: types.CallbackQuery):
    work_mode = await get_work_mode_db()
    print('click')

    if work_mode == 0:
        print('Поменяли ')
        await update_work_mode_db(1)
        markup = await markup_work_mode(1)
    elif work_mode == 1:
        await update_work_mode_db(0)
        markup = await markup_work_mode(0)
    await call.message.edit_reply_markup(markup)

    # await update_work_mode(call)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(update_work_mode, text=["update_work_mode"])
    dp.register_callback_query_handler(update_work_mode_click, text=["click_update_work_mode"])