import asyncio

import aiogram.utils.exceptions
from aiogram import types, Dispatcher
from os import remove
from keyboards.admin_kb import markup_mailing, markup_confirm_mailing
from keyboards.menu_kb import inline_kb_back_in_menu
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data_base.profile_db import get_all_users
from create_bot import bot, admin_id
class Mailing(StatesGroup):
    content = State()
    text_mailing = State()
async def mailing(call: types.CallbackQuery):
    await call.message.edit_caption('Выберите тип рассылки', reply_markup=(await markup_mailing()))

async def mailing_get_mailing_msg(call: types.CallbackQuery, state: FSMContext):
    chosen_btn = call.data.split('~')
    async with state.proxy() as data:
        data['content'] = chosen_btn[1]
    if chosen_btn[1] == 'text':
        await call.message.edit_caption('Введите текст для рассылки', reply_markup=inline_kb_back_in_menu)
    if chosen_btn[1] == 'photo_and_text':
        await call.message.edit_caption('Отправьте фото с описанием', reply_markup=inline_kb_back_in_menu)
    await Mailing.content.set()
async def mailing_get_mailing_msg_phase2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chosen_content = data['content']
    if chosen_content == 'text':
        try:
            with open("mailing.txt", "w", encoding="utf-8") as f:
                f.write(str(msg.text))
            await msg.answer(msg.text, parse_mode='html', reply_markup=(await markup_confirm_mailing()))
            await Mailing.text_mailing.set()
        except aiogram.utils.exceptions.MessageTextIsEmpty:
            await msg.answer('Повторите попытку', reply_markup=inline_kb_back_in_menu)
        except aiogram.utils.exceptions.CantParseEntities:
            await msg.answer("Повторите попытку\nОшибка в тегах '<' или '>', но, может, вы забыли закрывающий тег, к примеру: '</b>'", reply_markup=inline_kb_back_in_menu)
    elif chosen_content == 'photo_and_text':
        try:
            await msg.photo[-1].download(destination_file="mailing.jpg")
            with open("mailing.txt", "w", encoding="utf-8") as f:
                f.write(str(msg.caption))
            await bot.send_photo(chat_id=admin_id, photo=open("mailing.jpg", "rb"), caption=msg.caption, reply_markup=(await markup_confirm_mailing()))
            await Mailing.text_mailing.set()
        except IndexError:
            await msg.answer('Повторите попытку', reply_markup=inline_kb_back_in_menu)
async def confirm_and_start_mailing(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        chosen_content = data['content']
    ids = await get_all_users()
    print(ids)
    dontsend = ''
    count = 0
    if chosen_content == 'text':
        text_mailing = open("mailing.txt", "r", encoding="utf-8").read()
        for i in ids:
            try:
                await bot.send_message(chat_id=i[0], parse_mode='html', text=text_mailing)
            except (aiogram.utils.exceptions.CantInitiateConversation, aiogram.utils.exceptions.BotBlocked, aiogram.utils.exceptions.ChatNotFound):
                dontsend = f'{dontsend} {i[0]};'
                count = count + 1
            except:
                dontsend = f'{dontsend} {i[0]};'
                count = count + 1
            await asyncio.sleep(15e-3) # 5 ms sleep
        try:
            remove('mailing.txt')
        except:
            pass
    elif chosen_content == 'photo_and_text':
        text_mailing = open("mailing.txt", "r", encoding="utf-8").read()
        for i in ids:
            try:
                await bot.send_photo(chat_id=i[0], photo=open("mailing.jpg", "rb"), caption=text_mailing, parse_mode='html')
            except (aiogram.utils.exceptions.CantInitiateConversation, aiogram.utils.exceptions.BotBlocked, aiogram.utils.exceptions.ChatNotFound):
                dontsend = f'{dontsend} {i[0]};'
                count = count + 1
            except:
                dontsend = f'{dontsend} {i[0]};'
                count = count + 1
            await asyncio.sleep(15e-3) # 5 ms sleep

        try:
            remove("mailing.jpg")
            remove('mailing.txt')
        except:
            pass
    total_users = len(ids)
    await bot.send_message(call.from_user.id, f"Рассылка окончена\nНе получили рассылку след. USERы({count}/{total_users} юзеров не получили):\n\n{dontsend}")
    await state.finish()
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(mailing, text=["mailing"])
    dp.register_callback_query_handler(mailing_get_mailing_msg, text_startswith=["mailing~"])
    dp.register_message_handler(mailing_get_mailing_msg_phase2, content_types=["photo", "text"], state=Mailing.content)
    dp.register_callback_query_handler(confirm_and_start_mailing, text=["confirmmailing"], state=Mailing.text_mailing)


