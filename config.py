import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from data_base import sql_db


YOOTOKEN = os.getenv('YOOTOKEN')
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
db = sql_db.Database("users.db")