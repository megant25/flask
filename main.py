import telebot
from flask import Flask, request
from threading import Thread
import time
import random
import schedule
import datetime
import os

# Ambil token dari environment variable Railway
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
user_curhat = {}

# Setup Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook set!"

@app.route("/" + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

def run():
    app.run(host='0.0.0.0', port=8080)  # Railway hanya buka port 8080

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Daftar ID target pesan otomatis
TARGET_CHAT_IDS = [5379888876, 989898123]

# Notifikasi saat bot aktif
def notifikasi_bot_hidup():
    waktu_jakarta = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    jam = waktu_jakarta.strftime("%H:%M")
    tanggal = waktu_jakarta.strftime("%Y-%m-%d")
    pesan = f"🔄 Bot baru saja aktif kembali ({tanggal} jam {jam} WIB).\nKalau sempat off, maaf ya 🙏"
    for user_id in TARGET_CHAT_IDS:
        try:
            bot.send_message(user_id, pesan)
        except Exception as e:
            print(f"Error kirim notifikasi: {e}")

notifikasi_bot_hidup()

# --- Pesan Otomatis ---
def kirim_pesan_pagi():
    pesan_pagi = [
        "Selamat pagi! Semoga kamu bangun dengan senyum 💛",
        "Hai kamu yang jauh di sana... semangat pagi ya! 🌅",
        "Udara pagi segar, tapi lebih segar senyum kamu 😌☀️",
        "Pagi ini cuma pengen bilang: aku doain harimu menyenangkan 🤍",
        "Selamat pagi 🌞 jangan lupa sarapan dan jaga hati!"
    ]
    for user_id in TARGET_CHAT_IDS:
        try:
            bot.send_message(user_id, random.choice(pesan_pagi))
        except:
            pass

def kirim_pesan_siang():
    pesan_siang = [
        "Selamat siang! Jangan lupa makan ya 🍛",
        "Lagi sibuk nggak? Tapi jangan sampai lupa istirahat ya 😌",
        "Kalau kamu lelah, jangan dipaksa. Rehat bentar juga nggak apa 😴",
        "Siang ini cocok untuk kamu tetap semangat 💪✨"
    ]
    for user_id in TARGET_CHAT_IDS:
        try:
            bot.send_message(user_id, random.choice(pesan_siang))
        except:
            pass

# Jadwal
def job_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Waktu Indonesia Barat
schedule.every().day.at("07:00").do(kirim_pesan_pagi)
schedule.every().day.at("12:00").do(kirim_pesan_siang)
Thread(target=job_scheduler).start()

# --- Commands ---
@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    teks = (
        "👋 Hai! Aku bot curhat & penyemangat 🌟\n\n"
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
    bot.reply_to(message, "Terima kasih sudah berbagi. Semoga hatimu lebih lega 🤍")

# Polling dinonaktifkan karena pakai webhook
# bot.infinity_polling()
