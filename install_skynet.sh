#!/bin/bash
# Обновление системы и установка зависимостей
echo "[+] Обновление системы..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git wget curl unzip tmux build-essential python3 python3-pip python-is-python3 python3-dev

# Установка необходимых Python библиотек
echo "[+] Установка Python-библиотек..."
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install transformers diffusers accelerate xformers gradio pydub opencv-python sentence-transformers langchain whisper openai bitsandbytes aiohttp requests beautifulsoup4 lxml telethon pyrogram aiogram yt-dlp fastapi uvicorn python-dotenv

# Установка дополнительного пакета для обработки изображений
pip install pillow

echo "[+] Установка завершена. Запуск Skynet..."
