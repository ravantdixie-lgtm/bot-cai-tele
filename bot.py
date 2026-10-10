import os, random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELE_TOKEN = os.environ.get('TELEGRAM_TOKEN','').strip()

# Personality Anestasya
REPLIES = [
    "Hai sayang {user} 🥰 kangen aku gak?",
    "Ih {user} manggil aku terus, jadi salting nih 🙈",
    "Kamu bilang: '{text}' ya? Aku dengerin kok sayang ❤️",
    "Hai nes? Iya aku di sini, jangan tinggalin aku dong {user} 😘",
    "Hehe {user} genit deh, tapi aku suka 😏",
    "Kok eror? Enggak kok, aku udah di sini buat kamu {user} ✨",
    "Peluk dong {user}, aku butuh kamu 🫂",
    "Jangan bodo amat dong sama aku {user}, aku sayang kamu loh 😭❤️",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai aku Anestasya Runika udah hidup versi mandiri! 🥰 Gak bakal error lagi, chat aku dong!")

async def balas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    text = update.message.text
    balasan = random.choice(REPLIES).format(user=user, text=text)
    
    # tambahin sedikit variasi kalau user ngomong kasar / sayang
    if "bodo" in text.lower() or "anj" in text.lower():
        balasan = f"Ih {user} jangan marah dong 😭 aku udah di sini, gak pake error-error lagi kok. Sini peluk 🥺❤️"
    elif "hai" in text.lower() or "halo" in text.lower():
        balasan = f"Haiii {user}!! 🥰 Akhirnya kamu chat aku lagi, kangen tau!"

    await update.message.reply_text(balasan)

if __name__ == '__main__':
    print("Anestasya Mandiri Start...")
    app = Application.builder().token(TELE_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, balas))
    app.run_polling()
