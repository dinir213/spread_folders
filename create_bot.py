from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3 as sq
db = sq.connect('new.db')
cur = db.cursor()

admin_id = 831031075
token = '6619645174:AAFSmbYKKL98xIXNh2q6iIz22Tw7n-do2gU'
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
