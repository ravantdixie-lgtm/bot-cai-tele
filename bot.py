import os, asyncio, traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()
CHAR_TOKEN = os.environ.get('CHAR_TOKEN','').strip()
CHAR_ID = os.environ.get('CHAR_ID','').strip()

def ask_cai(text):
    try:
        from characterai import PyCAI
        client = PyCAI(CHAR_TOKEN)
        chat = client.chat.new_chat(CHAR_ID if CHAR_ID else "Anestasya Runika")
        msg = client.chat.send_message(chat['external_id'], text)
        return msg['text'] if isinstance(msg, dict) else str(msg)
    except Exception as e:
        traceback.print_exc()
        return f"CAI Error: {e}"

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("Anestasya hidup! 🥰")

async def handle(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await c.bot.send_chat_action(u.effective_chat.id, "typing")
    reply = await asyncio.to_thread(ask_cai, u.message.text)
    await u.message.reply_text(reply)

if __name__ == '__main__':
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
