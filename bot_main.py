import asyncio
from config import dp
from aiogram.utils import executor
from handlers import other, admin, client

client.registration_client(dp)
admin.registration_send_admin(dp)
other.register_send(dp)


async def user_check_sub(sleep_time):
    while True:
        task1 = asyncio.create_task(client.time_ban_user())
        await task1
        await asyncio.sleep(sleep_time)


async def on_start(_):
    asyncio.create_task(user_check_sub(100))
    print("Бот вышел в онлайн")


executor.start_polling(dp, skip_updates=True, on_startup=on_start)
