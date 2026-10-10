import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Kamu bilang: {update.message.text} - Bot Hidup!")

if __name__ == '__main__':
    print(f"Token panjang: {len(TELE_TOKEN)} - Bot jalan...")
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    app.run_polling()
