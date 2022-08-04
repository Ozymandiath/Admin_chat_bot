from aiogram import types, Dispatcher
from config import db, bot
from keyboards import kb_admin


# user_username = f"@{(await bot.get_chat(1325846378))['username']}"
async def verification_admin(message: types.Message):
    if db.admin_check(message.from_user.id):
        await bot.send_message(message.from_user.id, "Секретная настройка бота:", reply_markup=kb_admin)
    else:
        await bot.send_message(message.from_user.id, "Доступ к настройке бота есть только у админа.")


def registration_send_admin(dp: Dispatcher):
    dp.register_message_handler(verification_admin, text="Настройки бота")
