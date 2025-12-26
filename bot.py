import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import time

# تنظیمات
BOT_TOKEN = "8590467824:AAHNh6L2HKusWZhPGX4SLWyWFM096UHQ40A"
GITHUB_USERNAME = "Moeindevvvv"
REPO_NAME = "sadminix-miniapp1"
MINI_APP_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"

bot = telebot.TeleBot(BOT_TOKEN)
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users[user_id] = {
        'name': message.from_user.first_name,
        'start_time': time.time()
    }
    
    markup = InlineKeyboardMarkup(row_width=1)
    
    # دکمه وب‌اپ
    web_app_btn = InlineKeyboardButton(
        text="🚀 اجرای مینی‌اپ",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    markup.add(web_app_btn)
    markup.add(
        InlineKeyboardButton("📖 آموزش", callback_data="help"),
        InlineKeyboardButton("🔗 لینک مستقیم", url=MINI_APP_URL),
        InlineKeyboardButton("⭐ کانال ما", url="https://t.me/sadminix")
    )
    
    text = f"""
👋 سلام {message.from_user.first_name}!

🎯 **بات مینی‌اپ Sadminix** فعال شد.

🌐 **آدرس مینی‌اپ شما:**
{MINI_APP_URL}

📱 روی دکمه زیر کلیک کنید تا مینی‌اپ زیبا باز شود:
"""
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = """
🆘 **راهنمای استفاده:**

1. دستور `/start` - نمایش منوی اصلی
2. روی دکمه «اجرای مینی‌اپ» کلیک کنید
3. مینی‌اپ در پنجره جدید باز می‌شود
4. از دکمه‌های داخل مینی‌اپ استفاده کنید

🔧 **اگر مینی‌اپ باز نشد:**
• مطمئن شوید GitHub Pages فعال است
• لینک را مستقیماً باز کنید: """ + MINI_APP_URL + """

📞 **پشتیبانی:** @Sadminix
"""
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['link'])
def send_link(message):
    bot.send_message(
        message.chat.id,
        f"🔗 لینک مستقیم مینی‌اپ:\n{MINI_APP_URL}\n\nبرای بازکردن کلیک کنید.",
        disable_web_page_preview=True
    )

@bot.message_handler(commands=['stats'])
def stats(message):
    user_id = message.from_user.id
    if user_id in users:
        user = users[user_id]
        uptime = int(time.time() - user['start_time'])
        
        text = f"""
📊 **آمار کاربری:**

👤 نام: {user['name']}
🆔 شناسه: {user_id}
⏱️ زمان فعال: {uptime} ثانیه
👥 کاربران کل: {len(users)}

🌐 لینک مینی‌اپ: {MINI_APP_URL}
"""
    else:
        text = "اول از دستور /start استفاده کنید."
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "help":
        help_cmd(call.message)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text.lower() == "سلام":
        bot.reply_to(message, f"سلام {message.from_user.first_name}! 👋\nبرای شروع /start رو بزن.")
    elif "مینی اپ" in message.text.lower():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازکردن مینی‌اپ", web_app=WebAppInfo(url=MINI_APP_URL)))
        bot.send_message(message.chat.id, "مینی‌اپ آماده است:", reply_markup=markup)
    else:
        bot.reply_to(message, "دستور /help رو بزن تا راهنمایی بگیرم.")

# اجرای بات
if __name__ == "__main__":
    print("="*50)
    print("🤖 بات مینی‌اپ Sadminix")
    print("="*50)
    print(f"🌐 آدرس مینی‌اپ: {MINI_APP_URL}")
    print("🔄 در حال اتصال به تلگرام...")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ خطا: {e}")
