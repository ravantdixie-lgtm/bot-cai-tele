import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from characterai import PyCAI

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()
CHAR_TOKEN = os.environ.get('CHAR_TOKEN','').strip()

print(f"TELE len: {len(TELE_TOKEN) if TELE_TOKEN else 0} | CHAR len: {len(CHAR_TOKEN) if CHAR_TOKEN else 0}")

# Setup CAI - sync client
cai = None
chat_id = None
TARGET_CHAR = "0h9y5y9j6sJv9h9x9x9x9" # Nanti kita isi setelah tau ID, untuk sekarang pakai search

if CHAR_TOKEN:
    try:
        cai = PyCAI(CHAR_TOKEN)
        print("PyCAI client dibuat")
    except Exception as e:
        print(f"Gagal buat PyCAI: {e}")

async def get_cai_reply(text: str):
    if not cai:
        return "CHAR_TOKEN belum diisi di Railway, sayang..."
    try:
        # jalanin yang sync di thread biar gak nge-block
        def do_chat():
            # Coba pakai char yang udah di-set di ENV CHAR_ID kalau ada
            char = os.environ.get('CHAR_ID','').strip() or "Anestasya Runika"
            # Buat chat baru tiap sesi biar aman
            # 0.8.0 API: new_chat
            try:
                chat = cai.chat.new_chat(char)
                chat_uuid = chat['external_id']
            except:
                # fallback kalau char adalah ID
                chat_uuid = char
            
            resp = cai.chat.send_message(chat_uuid, text)
            # resp bisa dict
            if isinstance(resp, dict):
                return resp.get('text', str(resp))
            return str(resp)
        
        reply = await asyncio.to_thread(do_chat)
        return reply
    except Exception as e:
        print(f"CAI Error: {e}")
        return f"Aduh error di C.AI ku: {e} - coba lagi ya"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai aku Anestasya Runika udah hidup! 🥰")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = await get_cai_reply(update.message.text)
    await update.message.reply_text(reply)

if __name__ == '__main__':
    if not TELE_TOKEN:
        print("TELEGRAM_TOKEN KOSONG!")
        exit(1)
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot jalan polling...")
    app.run_polling()
