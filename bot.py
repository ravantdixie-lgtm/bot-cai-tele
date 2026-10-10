import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from characterai import PyCAI

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAR_TOKEN = os.environ.get('CHAR_TOKEN')
CHAR_ID = "eaC102LU5UioIjQUKYR8GOUATvjYUkjwNwo8pQqCa1g"

client = PyCAI(CHAR_TOKEN)
print("Bot jalan...")

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        txt = update.message.text
        print(f"User: {txt}")
        chat = client.chat.new_chat(CHAR_ID)
        res = client.chat.send_message(CHAR_ID, chat['external_id'], txt)
        await update.message.reply_text(res['text'])
    except Exception as e:
        print(f"ERROR: {e}")
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    app.run_polling()
    
