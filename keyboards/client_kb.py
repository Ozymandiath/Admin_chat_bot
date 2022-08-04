from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup

start_b1 = KeyboardButton("Подписка")
start_b2 = KeyboardButton("Рефералы")
start_b3 = KeyboardButton("Настройки бота")

kb_client_start = ReplyKeyboardMarkup(resize_keyboard=True).add(start_b1).add(start_b2).add(start_b3)

sub_b1 = KeyboardButton("Оплата")
sub_b2 = KeyboardButton("Статистика")
sub_b3 = KeyboardButton("Осталось")
sub_b4 = KeyboardButton("Вступить")
sub_b5 = KeyboardButton("Назад")

kb_client_sub = ReplyKeyboardMarkup(resize_keyboard=True).row(sub_b1, sub_b2, sub_b3).add(sub_b4).add(sub_b5)

inl_sub1 = InlineKeyboardButton("Карта ", callback_data="payment_by_card")
inl_sub2 = InlineKeyboardButton("Криптовалюта ", callback_data="payment_crypto")

kb_client_inline = InlineKeyboardMarkup(row_width=1).insert(inl_sub1).insert(inl_sub2)
