import os
from gtts import gTTS
import gradio as gr
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image
import requests
from io import BytesIO
import asyncio
import threading

# === Telegram Bot Setup ===
TELEGRAM_TOKEN = "8093963383:AAEU_HsVmhRdSE0kK6wGtF7W5yOgHhxUnvI"
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# === Global State ===
mode = {"type": "text"}  # or "voice"
chat_history = []

# === Web UI Logic ===
def chat_web(input_text):
    response = f"[Skynet] Я получил: {input_text}"
    chat_history.append((input_text, response))
    if mode["type"] == "voice":
        tts = gTTS(text=response, lang='ru')
        tts.save("response.mp3")
        return chat_history, "response.mp3", None
    else:
        return chat_history, None, None

def generate_image(prompt):
    img_url = "https://picsum.photos/512"
    img = Image.open(BytesIO(requests.get(img_url).content))
    return img

def toggle_mode(selected):
    mode["type"] = selected
    return f"Режим переключен на: {selected}"

def clear_history():
    chat_history.clear()
    return [], None, None

# === Gradio Interface ===
with gr.Blocks() as ui:
    gr.Markdown("# Skynet SEED — Web UI: Chat + Voice + Image + Telegram")
    txt = gr.Textbox(label="Введите сообщение")
    mode_selector = gr.Radio(["text", "voice"], value="text", label="Режим ответа", interactive=True)
    out_hist = gr.Chatbot(label="История диалога")
    out_audio = gr.Audio(label="Аудио", interactive=False)
    out_img = gr.Image(label="Сгенерированное изображение", interactive=False)
    gen_btn = gr.Button("Сгенерировать изображение")
    clear_btn = gr.Button("Очистить историю")

    mode_selector.change(fn=toggle_mode, inputs=mode_selector, outputs=out_hist)
    txt.submit(fn=chat_web, inputs=txt, outputs=[out_hist, out_audio, out_img])
    gen_btn.click(fn=generate_image, inputs=txt, outputs=out_img)
    clear_btn.click(fn=clear_history, outputs=[out_hist, out_audio, out_img])

def run_gradio():
    ui.launch(server_name="0.0.0.0", server_port=7860, share=False)

# === Telegram Logic ===
@dp.message_handler()
async def handle_message(message: types.Message):
    response = f"[Skynet] Я получил: {message.text}"
    if mode["type"] == "voice":
        tts = gTTS(text=response, lang='ru')
        tts.save("response.mp3")
        await message.reply_audio(open("response.mp3", "rb"), caption=response)
    else:
        await message.reply(response)

def run_telegram():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True)

# === Запуск в отдельных потоках ===
if __name__ == "__main__":
    threading.Thread(target=run_telegram, daemon=True).start()
    run_gradio()
