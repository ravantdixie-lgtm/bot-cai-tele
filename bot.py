import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from characterai import PyCAI

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAR_TOKEN = os.environ.get('CHAR_TOKEN')
CHAR_ID = "eaC102LU5UioIjQUKYR8GOUATvjYUkjwNwo8pQqCa1g"

print("Bot jalan...")

client = PyCAI(CHAR_TOKEN)

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"User: {text}")
    try:
        # buat chat baru
        data = client.chat.new_chat(CHAR_ID)
        chat_id = data['external_id']
        
        # kirim pesan
        msg = client.chat.send_message(CHAR_ID, chat_id, text)
        reply = msg['text']
        
        await update.message.reply_text(reply)
    except Exception as e:
        print(f"ERROR: {e}")
        await update.message.reply_text(f"Error CAI: {e}")

if __name__ == '__main__':
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    app.run_polling()
