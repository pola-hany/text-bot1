import os
import time
import requests
import telebot
from telebot import apihelper
from handlers import register_all_handlers

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

# إزالة webhook
try:
    requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', timeout=10)
    print("✅ تم حذف webhook")
except:
    pass

apihelper.ENABLE_MIDDLEWARE = False
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# تسجيل المعالجات
register_all_handlers(bot)

if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة يعمل...")
    try:
        print(f"🤖 @{bot.get_me().username}")
    except:
        print("🤖 جاري التشغيل...")
    print("=" * 50)
    
    while True:
        try:
            bot.polling(
                none_stop=True,
                interval=1,
                timeout=30,
                long_polling_timeout=30,
                skip_pending=True
            )
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            if "409" in str(e):
                try:
                    requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', timeout=5)
                except:
                    pass
                time.sleep(10)
            else:
                time.sleep(5)