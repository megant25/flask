import telebot
from flask import Flask, request
from threading import Thread
import time
import random
import schedule
import datetime
import os

TOKEN = os.getenv("BOT_TOKEN")  # Gunakan env variable untuk keamanan
bot = telebot.TeleBot(TOKEN)
user_curhat = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@app.route("/" + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Daftar user yang akan dikirimi pesan otomatis
TARGET_CHAT_IDS = [5379888876, 989898123]

# ðŸ”” Kirim notifikasi saat bot aktif ulang
def notifikasi_bot_hidup():
    waktu_jakarta = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    jam = waktu_jakarta.strftime("%H:%M")
    tanggal = waktu_jakarta.strftime("%Y-%m-%d")
    pesan = f"ðŸ”„ Bot baru saja aktif kembali ({tanggal} jam {jam} WIB).\nKalau sempat off, maaf ya ðŸ™"
    for user_id in TARGET_CHAT_IDS:
        try:
            bot.send_message(user_id, pesan)
        except:
            pass

notifikasi_bot_hidup()

# --- Fungsi ucapan otomatis ---
def kirim_pesan_pagi():
    pesan_pagi = [
        "Selamat pagi! Semoga kamu bangun dengan senyum ðŸ’›",
        "Hai kamu yang jauh di sana... semangat pagi ya! ðŸŒ…",
        "Udara pagi segar, tapi lebih segar senyum kamu ðŸ˜Œâ˜€ï¸",
        "Pagi ini cuma pengen bilang: aku doain harimu menyenangkan ðŸ¤",
        "Selamat pagi ðŸŒž jangan lupa sarapan dan jaga hati!"
    ]
    for user_id in TARGET_CHAT_IDS:
        try:
            bot.send_message(user_id, random.choice(pesan_pagi))
        except:
            pass

def kirim_pesan_siang():
    pesan_siang = [
        "Selamat siang! Jangan lupa makan ya ðŸ›",
        "Lagi sibuk nggak? Tapi jangan sampai lupa istirahat ya ðŸ˜Œ",
        "Kalau kamu lelah, jangan dipaksa. Rehat bentar juga nggak apa ðŸ˜´",
        "Siang ini cocok untuk kamu tetap semangat ðŸ’¼âœ¨"
    ]
    for user_id in TARGET_CHAT_IDS:
        try:
            bot.send_message(user_id, random.choice(pesan_siang))
        except:
            pass

# Jadwal otomatis
def job_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("07:00").do(kirim_pesan_pagi)
schedule.every().day.at("12:00").do(kirim_pesan_siang)

Thread(target=job_scheduler).start()

# --- Command Handler ---
@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    teks = (
        "ðŸ‘‹ Hai! Aku bot curhat & penyemangat ðŸŒŸ\n\n"
        "/curhat - kirim curhatmu\n"
        "/help - tampilkan bantuan ini"
    )
    bot.reply_to(message, teks)

@bot.message_handler(commands=['curhat'])
def mulai_curhat(message):
    user_curhat[message.chat.id] = True
    bot.reply_to(message, "Silakan ketik curhatmu. Aku di sini untuk mendengarkan...")

@bot.message_handler(func=lambda m: user_curhat.get(m.chat.id, False))
def simpan_curhat(message):
    user_curhat[message.chat.id] = False
    bot.reply_to(message, "Terima kasih sudah berbagi. Semoga hatimu lebih lega ðŸ¤")

# Jalankan polling jika diperlukan lokal
# bot.infinity_polling()  <-- tidak dipakai saat pakai webhook
def run():
    app.run(host="0.0.0.0", port=8080)
