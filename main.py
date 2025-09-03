import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
RUNWAY_KEY = os.getenv("RUNWAY_API_KEY")

def generate_image(prompt: str):
    url = "https://api.runwayml.com/v1/query"
    headers = {"Authorization": f"Bearer {RUNWAY_KEY}"}
    data = {
        "input": prompt,
        "model": "stable-diffusion-v1-5"
    }
    r = requests.post(url, headers=headers, json=data)
    return r.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши запрос, и я сгенерирую картинку 🖼️")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("⏳ Генерирую...")
    result = generate_image(prompt)

    if "output" in result:
        image_url = result["output"][0]
        await update.message.reply_photo(photo=image_url)
    else:
        await update.message.reply_text("Ошибка генерации 😢")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()