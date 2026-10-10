import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from characterai import aiocai

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAR_TOKEN = os.environ['CHAR_TOKEN']
CHAR_ID = "eaC102LU5UioIjQUKYR8GOUATvjYUkjwNwo8pQqCa1g"

client = aiocai.Client(CHAR_TOKEN)

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        me = await client.get_me()
        chat = await client.connect()
        new, answer = await chat.new_chat(CHAR_ID, me.id)
        msg = await chat.send_message(CHAR_ID, new.chat_id, update.message.text)
        await update.message.reply_text(msg.text)
    except Exception as e:
        await update.message.reply_text(f"Token C.AI expired, ambil lagi. Error: {e}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
print("Bot Railway jalan...")
app.run_polling()
