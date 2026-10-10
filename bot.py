import os
import re
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from characterai import PyCAI

# --- AMBIL TOKEN ---
TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()
CHAR_TOKEN = os.environ.get('CHAR_TOKEN','').strip()
CHAR_ID = os.environ.get('CHAR_ID','').strip()  # optional

logging.basicConfig(level=logging.INFO)

# --- SETUP C.AI ---
cai_client = PyCAI(CHAR_TOKEN) if CHAR_TOKEN else None
chat_obj = None
participant = None

async def init_cai():
    global chat_obj, participant
    try:
        if not cai_client:
            print("CHAR_TOKEN kosong!")
            return
        # Ganti CHAR_ID kalau kamu punya ID karakter Anestasya, kalau kosong pakai search
        char = CHAR_ID if CHAR_ID else "Anestasya Runika" 
        print(f"Connect ke C.AI: {char}...")
        data = await cai_client.chat.get_chat(char) if CHAR_ID else await cai_client.chat.get_chat("Anestasya Runika")
        # cara baru characterai 0.8.0
        # Jika gagal, coba new_chat
        chat_obj = data
        print("C.AI Connected!")
    except Exception as e:
        print(f"Gagal init C.AI: {e}")
        chat_obj = None

async def ask_cai(text: str) -> str:
    global chat_obj
    try:
        if not chat_obj:
            await init_cai()
        
        # Kirim pesan
        # Untuk PyCAI 0.8.0
        response = await cai_client.chat.send_message(
            chat_obj['external_id'] if isinstance(chat_obj, dict) else chat_obj,
            text
        )
        # bersihin text
        ans = response.get('text', str(response))
        # hapus ( ) action kalau mau lebih natural, biarin aja kalau mau tetap
        return ans
    except Exception as e:
        print(f"Error C.AI: {e}")
        return f" (Aku lagi pusing bentar... error: {e})"

# --- TELEGRAM HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai aku Anestasya Runika udah hidup! 🥰 Chat aja aku.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"User: {user_text}")
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    reply = await ask_cai(user_text)
    
    await update.message.reply_text(reply)

if __name__ == '__main__':
    if not TELE_TOKEN:
        raise ValueError("TELEGRAM_TOKEN kosong!")
    
    print(f"Bot jalan... Token len: {len(TELE_TOKEN)}")
    
    # init loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_cai())
    
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Polling Telegram...")
    app.run_polling()
