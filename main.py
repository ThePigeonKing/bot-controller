import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
import asyncio
# from aiogram.utils import executor
import psutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
if TELEGRAM_API_KEY is None:
    raise ValueError("TELEGRAM API KEY is None!")
AUTHORIZED_USERNAMES = os.getenv("AUTHORIZED_USERNAMES").split(',')
if AUTHORIZED_USERNAMES is None:
    raise ValueError("AUTHORIZED_USERNAMES is None!")

# Initialize bot and dispatcher with memory storage
storage = MemoryStorage()
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()
# dp.middleware.setup(LoggingMiddleware())

# Check if user is authorized
def is_user_authorized(username):
    return username in AUTHORIZED_USERNAMES

# Command handlers
@dp.message(Command('lock'))
async def lock(message: Message):
    if not is_user_authorized(message.from_user.username):
        await message.answer("Unauthorized user.")
        return
    os.system('rundll32.exe user32.dll,LockWorkStation')  # For Windows
    await message.answer('Locked the PC!')

@dp.message(Command('reboot'))
async def reboot(message: Message):
    if not is_user_authorized(message.from_user.username):
        await message.answer("Unauthorized user.")
        return
    os.system('shutdown /r /t 1')  # For Windows
    await message.answer('Rebooting the PC!')

@dp.message(Command('stats'))
async def stats(message: Message):
    if not is_user_authorized(message.from_user.username):
        await message.answer("Unauthorized user.")
        return
    logged_in_users = {user.name for user in psutil.users()}
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    reply_message = (
        f'Logged-in Users: {", ".join(logged_in_users)}\n'
        f'CPU Usage: {cpu}%\n'
        f'Memory Usage: {memory}%'
    )
    await message.answer(reply_message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Started polling...")
    asyncio.run(main())
