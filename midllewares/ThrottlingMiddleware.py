import time

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram import types
from aiogram.types import CallbackQuery
from data_base.admin_db import get_work_mode_db
from create_bot import admin_id
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5):
        BaseMiddleware.__init__(self)
        self.rate_limit = limit
    async def on_process_message(self, msg: types.Message, data: dict):
        work_mode = await get_work_mode_db()
        if work_mode == 0:
            if msg.from_user.id != admin_id:
                await msg.reply('На данный момент на сервере бота идут технические работы, мы обязательно скоро вернемся 😉')
                raise CancelHandler()
            else:
                await msg.reply(f'Бот находится в выключенном состоянии для пользователей, кроме <i>Администратора {msg.from_user.first_name}</i> 😊', parse_mode='html')
    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        timestart = time.time_ns()
        work_mode = await get_work_mode_db()
        if work_mode == 0:
            if call.from_user.id != admin_id:
                try:
                    await call.message.edit_caption('На данный момент на сервере бота идут технические работы, мы обязательно скоро вернемся 😉')
                except:
                    await call.message.edit_text('На данный момент на сервере бота идут технические работы, мы обязательно скоро вернемся 😉')
                print("Время работы миддлваря:", time.time_ns() - timestart)
                raise CancelHandler()
            else:
                await call.answer(f'Бот для других выключен 😊')
        print("Время работы миддлваря:", time.time_ns() - timestart)