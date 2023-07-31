from aiogram import types, Dispatcher
from data_base import tov_or_paym_menu_db
from keyboards.num_buttons import kb_num_buttons
from create_bot import bot
async def click_handler(call: types.CallbackQuery):
    text = call.data.split(":")
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
            await call.message.edit_text(f'Для пополнения счета введите суммы, которую хотите пополнить: {btn} руб', reply_markup=(await kb_num_buttons()))
        except:
            pass
        await tov_or_paym_menu_db.update_value_amount_in_menu_payment(call, btn)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(click_handler, text_startswith=["deposit:"])
