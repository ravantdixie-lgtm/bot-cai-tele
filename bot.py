import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()
CHAR_TOKEN = os.environ.get('CHAR_TOKEN','').strip()
CHAR_ID = os.environ.get('CHAR_ID','').strip() or "Anestasya Runika" # isi ID karakter kalau punya

print(f"Bot start | TELE: {len(TELE_TOKEN)} | CHAR_TOKEN: {len(CHAR_TOKEN) if CHAR_TOKEN else 0}")

# --- Fungsi Chat ke Character AI pakai requests ---
def ask_anestasya(text: str) -> str:
    if not CHAR_TOKEN:
        return f"(CHAR_TOKEN kosong) Kamu bilang: {text}"

    try:
        headers = {
            "Authorization": f"Token {CHAR_TOKEN}",
            "Content-Type": "application/json"
        }
        # Step 1: Buat / lanjut chat (pakai endpoint beta)
        # Ini endpoint yang dipakai PyCAI di dalamnya
        # Kalau CHAR_ID masih nama, kita coba search dulu via API chat
        # Untuk simpel, kita pakai endpoint histories

        # Buat chat baru
        create_url = "https://beta.character.ai/chat/history/create/"
        payload = {
            "character": CHAR_ID,
            "tgt": CHAR_ID,
            "history_external_id": None
        }
        # Coba beberapa format, kalau gagal fallback ke echo
        try:
            r = requests.post(create_url, json={"character": CHAR_ID}, headers=headers, timeout=15)
            # print(r.text[:200])
            data = r.json()
            hist_id = data.get('external_id') or data.get('id') or data.get('history_external_id')
        except:
            hist_id = None

        if not hist_id:
            # kalau gagal create, coba langsung send dengan char name sebagai history
            hist_id = CHAR_ID

        # Step 2: Kirim pesan
        send_url = "https://beta.character.ai/chat/history/msgs/create/"
        # atau /chat/history/msgs/send/
        # Coba 2 endpoint
        for url in [
            "https://beta.character.ai/chat/history/msgs/create/",
            "https://beta.character.ai/chat/history/msgs/send/"
        ]:
            try:
                resp = requests.post(url, json={
                    "history_external_id": hist_id,
                    "character": CHAR_ID,
                    "tgt": CHAR_ID,
                    "text": text,
                    "type": "TYPE_ONE_ON_ONE"
                }, headers=headers, timeout=20)
                if resp.status_code == 200:
                    j = resp.json()
                    # Ambil text balasan
                    txt = j.get('text') or j.get('turn',{}).get('candidates',[{}])[0].get('text') or j.get('message')
                    if txt:
                        return txt
            except Exception as e:
                continue

        return f"Maaf sayang, C.AI ku lagi error, tapi aku denger kamu bilang: {text}"

    except Exception as e:
        print(f"CAI requests error: {e}")
        return f"Aku lagi pusing bentar ({e}), tapi aku denger: {text}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai aku Anestasya Runika udah hidup! 🥰 Chat aku dong!")

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"User: {user_text}")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # jalanin requests yang sync di thread biar gak nge-lag
    import asyncio
    reply = await asyncio.to_thread(ask_anestasya, user_text)

    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    print("Polling Telegram...")
    app.run_polling()
