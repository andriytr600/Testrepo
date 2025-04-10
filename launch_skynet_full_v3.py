import os
import gradio as gr
from gtts import gTTS
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image
import requests
from io import BytesIO
import asyncio
import threading
import datetime
import speech_recognition as sr

# === Telegram Bot Setup ===
TELEGRAM_TOKEN = "8093963383:AAEU_HsVmhRdSE0kK6wGtF7W5yOgHhxUnvI"
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# === Global State ===
mode = {"type": "text"}  # 'text' or 'voice'
chat_history = []

# === Chat & Logging Logic ===
def log_message(user, text):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("chat_log.txt", "a") as f:
        f.write(f"{timestamp} {user}: {text}\n")

def chat_web(input_text):
    response = f"[Skynet] Я получил: {input_text}"
    chat_history.append({"role": "user", "content": input_text})
    chat_history.append({"role": "assistant", "content": response})
    log_message("WebUser", input_text)
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
    with open("chat_log.txt", "w") as f:
        f.write("")
    return [], None, None

def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            return text
        except sr.UnknownValueError:
            return "Не удалось распознать речь."
        except sr.RequestError:
            return "Ошибка при запросе к сервису распознавания."

# === Gradio UI ===
with gr.Blocks() as ui:
    gr.Markdown("# Skynet SEED v3 — Chat + Voice I/O + Telegram + Logging")
    txt = gr.Textbox(label="Введите сообщение")
    audio_input = gr.Audio(source="upload", type="filepath", label="Голосовой ввод (русский)")
    mode_selector = gr.Radio(["text", "voice"], value="text", label="Режим ответа", interactive=True)
    out_hist = gr.Chatbot(label="История диалога", type="messages")
    out_audio = gr.Audio(label="Ответ (аудио)", interactive=False)
    out_img = gr.Image(label="Сгенерированное изображение", interactive=False)
    gen_btn = gr.Button("Сгенерировать изображение")
    clear_btn = gr.Button("Очистить историю")

    mode_selector.change(fn=toggle_mode, inputs=mode_selector, outputs=out_hist)
    txt.submit(fn=chat_web, inputs=txt, outputs=[out_hist, out_audio, out_img])
    audio_input.change(fn=transcribe_audio, inputs=audio_input, outputs=txt)
    gen_btn.click(fn=generate_image, inputs=txt, outputs=out_img)
    clear_btn.click(fn=clear_history, outputs=[out_hist, out_audio, out_img])

def run_gradio():
    ui.launch(server_name="0.0.0.0", server_port=7860, share=False)

# === Telegram Logic ===
@dp.message_handler(commands=["voice", "text", "clear"])
async def handle_command(message: types.Message):
    if message.text == "/voice":
        mode["type"] = "voice"
        await message.reply("Режим переключён на голос.")
    elif message.text == "/text":
        mode["type"] = "text"
        await message.reply("Режим переключён на текст.")
    elif message.text == "/clear":
        chat_history.clear()
        with open("chat_log.txt", "w") as f:
            f.write("")
        await message.reply("История очищена.")

@dp.message_handler()
async def handle_message(message: types.Message):
    log_message("TelegramUser", message.text)
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

# === Запуск потоков ===
if __name__ == "__main__":
    threading.Thread(target=run_telegram, daemon=True).start()
    run_gradio()
