import os, asyncio, traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()
CHAR_TOKEN = os.environ.get('CHAR_TOKEN','').strip()
CHAR_ID = os.environ.get('CHAR_ID','').strip()

print(f"START | TELE {len(TELE_TOKEN)} | CHAR {len(CHAR_TOKEN)} | ID {CHAR_ID}")

def ask_cai(text):
    try:
        from characterai import PyCAI
        client = PyCAI(CHAR_TOKEN)
        # buat chat baru
        data = client.chat.new_chat(CHAR_ID if CHAR_ID else "Anestasya Runika")
        chat_id = data.get('external_id') or data.get('id')
        ans = client.chat.send_message(chat_id, text)
        if isinstance(ans, dict):
            return ans.get('text','(kosong)')
        return str(ans)
    except Exception as e:
        traceback.print_exc()
        return f"CAI Error detail: {e}"

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
    print("Polling...")
    app.run_polling()
