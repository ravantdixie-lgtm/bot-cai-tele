import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN')
print(f"Token ada? {TELE_TOKEN is not None} - Panjang: {len(TELE_TOKEN) if TELE_TOKEN else 0}")

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Kamu bilang: {update.message.text} - Bot Hidup!")

if __name__ == '__main__':
    if not TELE_TOKEN:
        print("ERROR: TELEGRAM_TOKEN KOSONG!")
        raise ValueError("TELEGRAM_TOKEN kosong di Railway!")
    
    print("Bot jalan tes...")
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    app.run_polling()
