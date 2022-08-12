from aiogram import types, Dispatcher

from config import db, bot
from keyboards import kb_client_start, kb_sub_inline, kb_sub_button


async def start_message(message: types.Message):
    if db.user_presence(message.from_user.id):
        start_msg = message.text
        referrer_id = str(start_msg[7:])
        if referrer_id != "":
            if referrer_id == str(message.from_user.id):
                await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!")
            else:
                db.add_user(message.from_user.id, referrer_id)
                await bot.send_message(message.from_user.id, "Вы зарегестрированы по реферальной ссылке")
                try:
                    await bot.send_message(int(referrer_id), "Ваш реферал зарегестрирован.")
                except:
                    pass
                await is_subscription_channel(message.from_user.id)
        else:
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "Вы зарегестрированы!")
            await is_subscription_channel(message.from_user.id)
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы!")
        await is_subscription_channel(message.from_user.id)


async def is_subscription_channel(user_id):
    user_info = await bot.get_chat_member(-1001779024448, user_id)
    if user_info["status"] == "left":
        await bot.send_message(user_id, "Вы должны быть подписчиком!", reply_markup=kb_sub_button)
        await bot.send_message(user_id, "Подпишитесь на канал:", reply_markup=kb_sub_inline)
    else:
        await bot.send_message(user_id, "Приятного трейдинга", reply_markup=kb_client_start)


async def get_subscription(message:types.Message):
    await message.delete()
    await is_subscription_channel(message.from_user.id)


async def minor_commands(message: types.Message):
    if message.text == "Назад":
        await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=kb_client_start)
    else:
        await bot.send_message(message.from_user.id, f"@{message.from_user.username}, такой команды нету.",
                               reply_markup=kb_client_start)


def register_send(dp: Dispatcher):
    dp.register_message_handler(start_message, commands="start")
    dp.register_message_handler(get_subscription, text="Подписался")
    dp.register_message_handler(minor_commands)

