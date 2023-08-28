from aiogram.utils import executor
from create_bot import dp
from data_base import start_db

from midllewares.ThrottlingMiddleware import ThrottlingMiddleware
# Регистрация мидлваря:
def register_all_middlewares(dp):
    dp.middleware.setup(ThrottlingMiddleware())
# Регистрация Всех хендлеров:
def register_all_handlers_client(dp):
    from handlers import start_handler, menu_collbacks, num_click_handler, buy_handler
    start_handler.register_handlers_client(dp)
    menu_collbacks.register_handlers_client(dp)
    buy_handler.register_handlers_client(dp)
    num_click_handler.register_handlers_client(dp)
    from payment_process import payment_process
    payment_process.register_handlers_client(dp)
    from admin import admin_panel, add_payment_methods, add_tov, update_percent_referral, update_work_mode, mailing, statistic
    admin_panel.register_handlers_client(dp)
    add_payment_methods.register_handlers_client(dp)
    add_tov.register_handlers_client(dp)
    update_percent_referral.register_handlers_client(dp)
    update_work_mode.register_handlers_client(dp)
    mailing.register_handlers_client(dp)
    statistic.register_handlers_client(dp)
async def on_startup(_):
    start_db.db_start()
    print('Бот вышел в онлайн')
    register_all_middlewares(dp)
    register_all_handlers_client(dp)

if __name__ == "__main__":
    # dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)