import yt_dlp
import telebot

API_TOKEN = "8342188590:AAFR1c4yQSp1nQvC_aV88WQFoCYtRuOLg-M"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Надішли посилання на YouTube відео, і я його завантажу."
    )

@bot.message_handler(content_types=['text'])
def handle_message(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏳ Завантажую відео...")

    # Викликається частина Артема (бекенд)
    file_path = download_video(url)

    if file_path:
        bot.send_document(message.chat.id, open(file_path, "rb"))
        bot.send_message(message.chat.id, "✅ Готово!")
    else:
        bot.send_message(message.chat.id, "❌ Помилка при завантаженні.")

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path

    except Exception as e:
        print("Помилка:", e)
        return None


bot.polling()