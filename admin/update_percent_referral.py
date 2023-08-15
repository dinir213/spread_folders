from create_bot import bot
from data_base.admin_db import get_percent_referral_db, update_percent_referral_db
from aiogram import types, Dispatcher
from keyboards.menu_kb import inline_kb_back_in_menu
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
class Referrals(StatesGroup):
    percent_referral = State()
async def view_percent_referral(call: types.CallbackQuery):
    await Referrals.percent_referral.set()
    percent_referral = await get_percent_referral_db()
    await call.message.edit_text(f"Процент от каждой покупки приведенного Вами клиента составляет <b>{percent_referral}%</b>\n\nЧтобы изменить его, введите новое значение <i>(целое положительное число)</i>.\nДля выхода нажмите на <i>кнопку</i> 👇", reply_markup=inline_kb_back_in_menu, parse_mode='html')
async def update_percent_referral(message: types.Message, state: FSMContext):
    percent = message.text
    if percent.isdigit() and int(percent) > 0:
        await update_percent_referral_db(percent)
        await bot.send_message(message.from_user.id, f'Процент от покупки рефераллов изменен на <b>{int(percent)}%</b> <i>администратором <b>{message.from_user.first_name}</b></i> ✅', reply_markup=inline_kb_back_in_menu, parse_mode='html')
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Вы ввели неверное значение', reply_markup=inline_kb_back_in_menu)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(view_percent_referral, text=["update_percent_referral"])
    dp.register_message_handler(update_percent_referral, state=Referrals.percent_referral)