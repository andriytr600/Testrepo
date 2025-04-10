
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio

API_TOKEN = '8093963383:AAEU_HsVmhRdSE0kK6wGtF7W5yOgHhxUnvI'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class SkynetCore:
    def __init__(self):
        self.active = False

    def chat(self, message):
        return f"[SkynetCore ответ]: {message[::-1]}"

skynet = SkynetCore()

@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text.strip().lower()

    if user_input == "скай старт":
        await message.reply("Введите мастер-ключ для активации:")
        return

    if user_input == "lilit666":
        skynet.active = True
        await message.reply("**[Skynet активирован]** Ядро включено. Готов к работе.")
        return

    if skynet.active:
        response = skynet.chat(user_input)
        await message.reply(response)
    else:
        await message.reply(f"[Skynet] Я получил: {message.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
