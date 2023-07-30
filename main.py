from aiogram.utils import executor
from create_bot import dp

from data_base import start_db

async def on_startup(_):
    start_db.db_start()
    print('Бот вышел в онлайн')
from handlers import client, admin, other
client.register_handlers_client(dp)
other.register_handlers_other(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)