import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from characterai import aiocai

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAR_TOKEN = os.environ.get('CHAR_TOKEN')
CHAR_ID = "eaC102LU5UioIjQUKYR8GOUATvjYUkjwNwo8pQqCa1g"

print("Bot Railway jalan...")

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    print(f"User: {user_text}")
    try:
        client = aiocai.Client(CHAR_TOKEN)
        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(CHAR_ID, me.id)
            message = await chat.send_message(CHAR_ID, new.chat_id, user_text)
            await update.message.reply_text(message.text)
            print(f"Bot: {message.text}")
    except Exception as e:
        print(f"ERROR: {e}")
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    app.run_polling()
