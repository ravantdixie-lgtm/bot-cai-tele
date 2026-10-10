import os
import asyncio
import traceback
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()
CHAR_TOKEN = os.environ.get('CHAR_TOKEN','').strip()

print(f"START | TELE: {len(TELE_TOKEN)} | CHAR: {len(CHAR_TOKEN)}")

# Coba import CAI, kalau gagal bot tetep jalan
try:
    from characterai import PyCAI
    CAI_AVAILABLE = True
    print("characterai lib OK")
except Exception as e:
    CAI_AVAILABLE = False
    print(f"characterai lib GAGAL: {e}")

cai_client = None
if CAI_AVAILABLE and CHAR_TOKEN:
    try:
        cai_client = PyCAI(CHAR_TOKEN)
        print("PyCAI client OK")
    except Exception as e:
        print(f"PyCAI init gagal: {e}")
        cai_client = None

async def get_reply(text: str):
    if not cai_client:
        return f"Kamu bilang: {text} (CAI lagi off, tapi bot Telegram ku hidup!)"
    try:
        def sync_call():
            try:
                # coba new chat dengan search name
                chat = cai_client.chat.new_chat(os.environ.get('CHAR_ID','').strip() or "Anestasya Runika")
                chat_id = chat.get('external_id', chat.get('id'))
                msg = cai_client.chat.send_message(chat_id, text)
                if isinstance(msg, dict):
                    return msg.get('text', str(msg))
                return str(msg)
            except Exception as inner:
                traceback.print_exc()
                return f"Error CAI: {inner}"

        return await asyncio.to_thread(sync_call)
    except Exception as e:
        traceback.print_exc()
        return f"Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Anestasya hidup! 🥰")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        reply = await get_reply(update.message.text)
        await update.message.reply_text(reply)
    except Exception as e:
        print(f"Handle error: {e}")
        await update.message.reply_text(f"Error handle: {e}")

def main():
    try:
        if not TELE_TOKEN:
            print("FATAL: TELEGRAM_TOKEN kosong")
            # jangan exit biar gak crash loop, sleep aja
            import time
            while True:
                print("Menunggu TELEGRAM_TOKEN...")
                time.sleep(30)
        
        print("Build Application...")
        app = Application.builder().token(TELE_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
        print("Polling...")
        app.run_polling()
    except Exception as e:
        print(f"FATAL CRASH: {e}")
        traceback.print_exc()
        # sleep biar Railway gak restart terus
        import time
        while True:
            print("Crash loop sleep...")
            time.sleep(60)

if __name__ == '__main__':
    main()
