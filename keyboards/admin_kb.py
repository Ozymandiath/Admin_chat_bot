from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

all = KeyboardButton('Настройки')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(all)
