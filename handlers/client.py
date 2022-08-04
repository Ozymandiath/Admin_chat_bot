import time
import datetime
from aiogram import types, Dispatcher
from aiogram.types.message import ContentType
from config import db, bot, YOOTOKEN
from keyboards import kb_client_sub, kb_client_inline


def days_to_second(days):
    return days * 24 * 60 * 60


def get_remaining_time(get_time):
    middle_time = int(get_time) - int(time.time())
    return False if middle_time <= 0 else str(datetime.timedelta(seconds=middle_time))


async def time_ban_user():
    for i in db.user_list():
        user_info = await bot.get_chat_member(-1001664990040, i)
        if db.get_status_sub(i):
            if user_info["status"] == "kicked":
                await bot.unban_chat_member(chat_id=-1001664990040, user_id=i, only_if_banned=True)

                await bot.send_message(i, "Доступ возвращен. \nКнопка 'Вступить' снова активна.")
        else:
            if not user_info["status"] == "kicked":
                await bot.ban_chat_member(chat_id=-1001664990040, user_id=i)
                await bot.send_message(-1001664990040,
                                       f"У @{(await bot.get_chat(i))['username']}, закончилась подписка.")
                await bot.send_message(i, "Доступ в чат закрыт. \nПродлите подписку.")


async def subscription_making(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите нужное действие в меню:", reply_markup=kb_client_sub)


async def get_subscription_time(message: types.Message):
    check_time = get_remaining_time(db.get_time_sub(message.from_user.id))
    if check_time:
        check_time = check_time.replace(",", " и ")
        user_time = f"Подписка действует:  {check_time}"
    else:
        user_time = "Подписка отсутствует"
    await bot.send_message(message.from_user.id, user_time)


async def pay_subscription(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите способ оплаты:", reply_markup=kb_client_inline)


async def buy_sub_month(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title="Месячная подписка",
                           description="Подписка выдается на 1 месяц", payload="month_sub", provider_token=YOOTOKEN,
                           currency="RUB", start_parameter="sub_bot", prices=[{"label": "Руб", "amount": 80000}])


async def process_payment_sub(process: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(process.id, ok=True)


async def payment_confirmation(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        time_sub = int(time.time()) + days_to_second(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "Подписка успешно оплачена и добавлена.")


async def get_subscription_link(message: types.Message):
    link = await bot.export_chat_invite_link(chat_id=-1001664990040)
    if db.get_status_sub(message.from_user.id):
        await bot.send_message(message.from_user.id, f"VIP-канал: {link}")
    else:
        await bot.send_message(message.from_user.id, "Оплатите подписку")


def registration_client(dp: Dispatcher):
    dp.register_message_handler(subscription_making, text="Подписка")
    dp.register_message_handler(get_subscription_time, text="Осталось")
    dp.register_message_handler(pay_subscription, text="Оплата")
    dp.register_callback_query_handler(buy_sub_month, text="payment_by_card")
    dp.register_pre_checkout_query_handler(process_payment_sub)
    dp.register_message_handler(payment_confirmation, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(get_subscription_link, text="Вступить")
