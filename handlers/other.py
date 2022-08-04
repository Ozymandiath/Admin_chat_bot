from aiogram import types, Dispatcher
from config import db, bot
from keyboards import kb_client_start

async def start_message(message: types.Message):
    if db.user_presence(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
        await bot.send_message(message.from_user.id, text="Вы зарегестрированы!", reply_markup=kb_client_start)
    else:
        if message.text == "Назад":
            await bot.send_message(message.from_user.id, text="Главное меню:", reply_markup=kb_client_start)
        else:
            await bot.send_message(message.from_user.id, text=f"@{message.from_user.username}, такой команды нету.",
                                   reply_markup=kb_client_start)


def register_send(dp: Dispatcher):
    dp.register_message_handler(start_message)

