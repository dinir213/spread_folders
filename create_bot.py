from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3 as sq
db = sq.connect('new.db')
cur = db.cursor()

token = '6130281935:AAHQXn1NRrzfLDG0Z8aR5Ez1kH9poG5V6F8'
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
