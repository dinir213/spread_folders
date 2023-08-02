from aiogram import types, Dispatcher
from keyboards.admin_kb import create_kb_payment_methods
from data_base.admin_db import turn_payment_method_db, view_all_payment_methods
from create_bot import bot
async def view_all_payment_methods(call: types.CallbackQuery):
    await call.message.edit_text(f"Включить способы оплаты можно путем нажатия на кнопку ниже с его названием", reply_markup=(await create_kb_payment_methods()))

async def turn_payment_method(call: types.CallbackQuery):
    paym_data = call.data.split(':')
    if paym_data[2] == '1':
        await turn_payment_method_db("0", paym_data[1])
    elif paym_data[2] == '0':
        await turn_payment_method_db("1", paym_data[1])
    await bot.answer_callback_query(call.id)

    inline_kb_add_payment_methods = await create_kb_payment_methods()
    await call.message.edit_reply_markup(inline_kb_add_payment_methods)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(view_all_payment_methods, text=["add_payment_methods"])
    dp.register_callback_query_handler(turn_payment_method, text_startswith=['turn_paym_method:'])