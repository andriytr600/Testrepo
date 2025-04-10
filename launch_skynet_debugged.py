import logging
import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv

from gpt_interface import ask_gpt

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))
MASTER_KEY = os.getenv("MASTER_KEY", "Lilit666")
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text.strip()
    print(">>> Запрос:", user_text)
    try:
        response = ask_gpt(user_text)
    except Exception as e:
        response = f"[Ошибка GPT]: {str(e)}"
    print(">>> Ответ:", response)
    await message.reply(response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
