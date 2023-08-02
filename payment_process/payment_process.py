from aiogram import types, Dispatcher
from data_base.tov_or_paym_menu_db import get_value_amount_in_menu_payment, update_payment_values_in_menu_payment, get_payment_values_in_menu_payment, del_payment_values_in_menu_payment
from data_base.profile_db import edit_profile
from payment_process import payment_json_requests
from keyboards.num_buttons import kb_check_payment_buttons
from keyboards import menu_kb
from create_bot import bot
async def get_check(call: types.CallbackQuery):
    text = call.data.split('_')
    amount = await get_value_amount_in_menu_payment(call)
    try:
        amount = amount.replace(',', '.')
        amount = float(amount)
    except ValueError:
        amount = 'string'
    if isinstance(amount, float) and amount >= 0.01:
        if text[1] == 'yookassa':
            payment_url = await payment_json_requests.create_payment(amount)
            await call.message.edit_text(f"Перейдите по ссылке для оплаты {amount} руб: {payment_url[0]}", reply_markup=(await kb_check_payment_buttons(text[1])))
            await update_payment_values_in_menu_payment(call, payment_url[1], '', '', text[1])
        elif text[1] == 'cryptomus':
            paym_data_crypto = await payment_json_requests.create_payment_cryptomus(amount)
            await call.message.edit_text(f"Перейдите по ссылке для оплаты {amount} RUB: {paym_data_crypto[0]}", reply_markup=(await kb_check_payment_buttons(text[1])))
            await update_payment_values_in_menu_payment(call, paym_data_crypto[1], paym_data_crypto[2], paym_data_crypto[3], text[1])
async def confirm_payment(call: types.CallbackQuery):
    payment_method = call.data.split('_')[1]
    if payment_method == 'yookassa':
        payment_data = await get_payment_values_in_menu_payment(call)
        payment_id = payment_data[3]
        amount = payment_data[1]
        payment_status = await payment_json_requests.check_payment(payment_id)
        payment_status = 'succeeded'
        if payment_status == 'waiting_for_capture':
            try:
                await call.message.edit_text('Для подтверждения платежа нажмите на кнопку "Оплачено" еще раз через 10 секунд', reply_markup=(await kb_check_payment_buttons(payment_method)))
            except:
                pass
        elif payment_status == 'pending':
            try:
                await call.message.edit_text('Не удалось произвести платеж, создайте новый счет и попробуйте оплатить', reply_markup=(await kb_check_payment_buttons(payment_method)))
            except:
                pass
        elif payment_status == 'succeeded':
            await edit_profile(call, amount)
            await call.answer('Успешно!')
            await del_payment_values_in_menu_payment(call)
            # await update_quantity_lost_accounts() Эта функция необходима для изменения кол-ва оставшившся товаров в таблице товаров
            await call.message.edit_text(f'Ваш баланс был успешно пополнен на {amount} руб\n\nДобро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
        elif payment_status == 'canceled':
            await call.message.edit_text(f'Вы отменили платеж\n Добро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
            await del_payment_values_in_menu_payment(call)
    elif payment_method == 'cryptomus':
        payment_data = await get_payment_values_in_menu_payment(call)
        print('payment_data: ', payment_data)
        payment_id = payment_data[3]
        amount = payment_data[1]
        payment_sing = payment_data[4]
        order_id = payment_data[5]
        payment_status = await payment_json_requests.check_payment_cryptomus(payment_id, order_id)
        payment_status = 'paid'
        if payment_status == 'check':
            try:
                await call.message.edit_text('Для подтверждения платежа нажмите на кнопку "Оплачено" еще раз через 10 секунд', reply_markup=(await kb_check_payment_buttons(payment_method)))
            except:
                pass
        elif payment_status == 'paid':
            await call.message.edit_text(f'Ваш баланс был успешно пополнен на {amount} руб\n\nДобро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
            await edit_profile(call, amount)
            print(f'user_id: {call.from_user.id}')
            await call.answer('Successfully!')
            await del_payment_values_in_menu_payment(call)

            # await update_quantity_lost_accounts()
        elif payment_status == 'cancel':
            await call.message.edit_text(f'Вы отменили платеж\n Добро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)
            await del_payment_values_in_menu_payment(call)
    elif payment_method == 'back':
        await del_payment_values_in_menu_payment(call)
        await call.message.edit_text(f'Добро пожаловать @{call.from_user.username}! Спасибо, что пользуетесь нашим магазином\n\nГлавное меню:', reply_markup=menu_kb.inline_kb_menu)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(get_check, text_startswith="getcheck_")
    dp.register_callback_query_handler(confirm_payment, text_startswith="successful.payment_")
