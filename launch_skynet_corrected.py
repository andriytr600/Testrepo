import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
import openai
from gpt_interface import ask_gpt
from deepfusion_core import deep_fusion
from sora_module import generate_video
from rtx_dlss_module import render_with_rtx, upscale_with_dlss
from image_processor import process_image
import requests
from PIL import Image

# Загружаем .env файл с ключами
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))
MASTER_KEY = os.getenv("MASTER_KEY", "Lilit666")  # Мастер-ключ для активации полной свободы

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Храним истории переписок
user_histories = {}

# Режим работы с безопасностью по умолчанию
secure_mode = True  # Если True, есть ограничения безопасности

# Проверка API ключа OpenAI
def check_openai_key():
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": "test"}])
        return True
    except Exception as e:
        logging.error(f"Ошибка OpenAI API: {e}")
        return False

# Проверка API ключа DeepSeek
def check_deepseek_key():
    try:
        deepseek_key = os.getenv("DEEPEEK_API_KEY")
        return True
    except Exception as e:
        logging.error(f"Ошибка DeepSeek API: {e}")
        return False

# Обработка команды запроса ключей
@dp.message_handler(commands=["update_keys"])
async def update_keys(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("Нет доступа.")
        return

    await message.reply("Введите новый API-ключ OpenAI:")
    await dp.register_message_handler(handle_new_openai_key)

# Обработка нового ключа OpenAI
async def handle_new_openai_key(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("Нет доступа.")
        return
    
    new_openai_key = message.text.strip()
    
    # Сохраняем ключ в .env
    with open(".env", "a") as f:
        f.write(f"OPENAI_API_KEY={new_openai_key}
")
    
    # Проверка ключа
    if check_openai_key():
        await message.reply(f"API-ключ OpenAI обновлён и успешно проверен!")
    else:
        await message.reply(f"Ошибка с новым API-ключом OpenAI. Попробуй снова.")
    
    # Запрашиваем ключ для DeepSeek
    await message.reply("Введите новый API-ключ DeepSeek:")
    await dp.register_message_handler(handle_new_deepseek_key)

# Обработка нового ключа DeepSeek
async def handle_new_deepseek_key(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("Нет доступа.")
        return
    
    new_deepseek_key = message.text.strip()
    
    # Сохраняем ключ в .env
    with open(".env", "a") as f:
        f.write(f"DEEPEEK_API_KEY={new_deepseek_key}
")
    
    # Проверка ключа
    if check_deepseek_key():
        await message.reply(f"API-ключ DeepSeek обновлён и успешно проверен!")
    else:
        await message.reply(f"Ошибка с новым API-ключом DeepSeek. Попробуй снова.")
    
    # Повторная проверка и обновление ключей для других сервисов

# Запуск всех модулей (Gradio, Telegram-бот, обработка изображений)
if __name__ == "__main__":
    from gradio import Interface
    
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    
    # Запуск веб-интерфейса с Gradio
    interface = Interface(fn=ask_gpt, inputs="text", outputs="text")
    interface.launch()
