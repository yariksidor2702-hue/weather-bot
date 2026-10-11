import telebot
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

def run_dummy_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        def log_message(self, *args):
            pass
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

Thread(target=run_dummy_server, daemon=True).start()
import requests

BOT_TOKEN = "8718393740:AAEY4Fwuf4OgsK4lo8U3TSEXV9vMrYjU7mU"
WEATHER_API_KEY = "aaf2d5b01ef619de39e73e6c6f84d749"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Напиши город, и я покажу погоду.")

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if r.status_code != 200:
            bot.reply_to(message, f"Город «{city}» не найден.")
            return
        text = (
            f"🌍 {city.capitalize()}\n"
            f"🌡 {data['main']['temp']:.1f}°C (ощущается {data['main']['feels_like']:.1f}°C)\n"
            f"☁️ {data['weather'][0]['description'].capitalize()}\n"
            f"💧 {data['main']['humidity']}%\n"
            f"💨 {data['wind']['speed']} м/с"
        )
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, "Ошибка. Попробуй позже.")
        print(e)

bot.polling(none_stop=True, skip_pending=True)
