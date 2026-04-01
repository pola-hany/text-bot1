import os
import time
import telebot
from handlers import register_all_handlers

# جلب التوكن
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

# إنشاء البوت
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# تسجيل جميع المعالجات
register_all_handlers(bot)

# إزالة webhook إذا كان موجوداً (لحل مشكلة 409)
try:
    bot.remove_webhook()
    print("✅ تم إزالة webhook")
except Exception as e:
    print(f"⚠️ خطأ في إزالة webhook: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة والترجمة المتقدم يعمل...")
    try:
        print(f"🤖 @{bot.get_me().username}")
    except:
        print("🤖 جاري تشغيل البوت...")
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
    
    # استخدام polling مع إعادة محاولة عند الخطأ
    while True:
        try:
            # polling بدون threading
            bot.polling(none_stop=True, interval=0, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ خطأ في polling: {e}")
            print("🔄 إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)
