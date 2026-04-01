import os
import time
import telebot
from telebot.types import ReplyKeyboardRemove
from handlers import register_all_handlers

# جلب التوكن
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

# إنشاء البوت مع إعدادات لمنع التعارض
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# تعطيل استخدام الـ threading لمنع التعارض
bot.config['threaded'] = False

# تسجيل جميع المعالجات
register_all_handlers(bot)

# إزالة webhook إذا كان موجوداً
try:
    bot.remove_webhook()
    print("✅ تم إزالة webhook")
except:
    pass

if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة والترجمة المتقدم يعمل...")
    print(f"🤖 @{bot.get_me().username}")
    print("=" * 50)
    print("📊 المميزات:")
    print("   🎨 25+ خط عربي")
    print("   🆎 11+ خط إنجليزي")
    print("   🇰🇷 8+ ترجمة كورية")
    print("   🇨🇳 8+ ترجمة صينية")
    print("   𓂀 8+ ترجمة فرعونية")
    print("   📝 200+ بايو لكل قسم")
    print("   🎨 تأثيرات إضافية")
    print("=" * 50)
    
    # استخدام polling عادي بدون threading
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            print("🔄 إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)