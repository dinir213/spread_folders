import json, string


from aiogram import types, Dispatcher

# @dp.message_handler()
async def echo_send(message: types.Message):
    if (message.text) == 'Мат':
        await message.reply('Маты запрещены')
        await message.delete()

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
