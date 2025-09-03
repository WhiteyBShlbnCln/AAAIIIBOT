import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
RUNWAY_KEY = os.getenv("RUNWAY_API_KEY")

def generate_from_runway(prompt: str, mode: str = "image"):
    url = "https://api.runwayml.com/v1/query"
    headers = {"Authorization": f"Bearer {RUNWAY_KEY}"}

    if mode == "image":
        data = {
            "input": prompt,
            "model": "stable-diffusion-v1-5"
        }
    elif mode == "video":
        data = {
            "input": prompt,
            "model": "gen-2"
        }
    else:
        return {"error": "Unknown mode"}

    try:
        r = requests.post(url, headers=headers, json=data, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! ✨\n"
        "Напиши `/img описание` для картинки 🖼️\n"
        "или `/vid описание` для видео 🎬"
    )

async def generate_image(update: U_
