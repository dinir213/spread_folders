from aiogram.utils import executor
from create_bot import dp

from data_base import start_db

async def on_startup(_):
    start_db.db_start()
    print('Бот вышел в онлайн')

from handlers import start_handler,  menu_collbacks, num_click_handler
start_handler.register_handlers_client(dp)
menu_collbacks.register_handlers_client(dp)
num_click_handler.register_handlers_client(dp)
from payment_process import payment_process
payment_process.register_handlers_client(dp)
from admin import admin_panel, add_payment_methods
admin_panel.register_handlers_client(dp)
add_payment_methods.register_handlers_client(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)