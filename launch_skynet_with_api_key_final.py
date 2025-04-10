import logging
import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
from gradio import Interface

from gpt_interface import ask_gpt
from deepfusion_core import deep_fusion
from sora_module import generate_video
from rtx_dlss_module import render_with_rtx, upscale_with_dlss
from image_processor import process_image

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))
MASTER_KEY = os.getenv("MASTER_KEY", "Lilit666")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_histories = {}
secure_mode = True

# Вставляем твой API ключ
openai.api_key = "{}".format(api_key)

def check_openai_key():
    try:
        openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        return True
    except Exception as e:
        logging.error(f"Ошибка OpenAI API: {e}")
        return False

def check_deepseek_key():
    try:
        deepseek_key = os.getenv("DEEPEEK_API_KEY")
        return True
    except Exception as e:
        logging.error(f"Ошибка DeepSeek API: {e}")
        return False

@dp.message_handler(commands=["update_keys"])
async def update_keys(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("Нет доступа.")
        return

    await message.reply("Введите новый API-ключ OpenAI:")
    await dp.register_message_handler(handle_new_openai_key)

async def handle_new_openai_key(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("Нет доступа.")
        return
    
    new_openai_key = message.text.strip()
    with open(".env", "a") as f:
        f.write(f"OPENAI_API_KEY={new_openai_key}\n")
    
    if check_openai_key():
        await message.reply("Ключ OpenAI успешно обновлён!")
    else:
        await message.reply("Ошибка проверки ключа OpenAI.")
    
    await message.reply("Введите новый API-ключ DeepSeek:")
    await dp.register_message_handler(handle_new_deepseek_key)

async def handle_new_deepseek_key(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("Нет доступа.")
        return
    
    new_deepseek_key = message.text.strip()
    with open(".env", "a") as f:
        f.write(f"DEEPEEK_API_KEY={new_deepseek_key}\n")
    
    if check_deepseek_key():
        await message.reply("Ключ DeepSeek успешно обновлён!")
    else:
        await message.reply("Ошибка проверки ключа DeepSeek.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    interface = Interface(fn=ask_gpt, inputs="text", outputs="text")
    interface.launch()
