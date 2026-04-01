import os
import time
import requests
import telebot
from telebot import apihelper
from handlers import register_all_handlers

# ============= إعدادات البوت =============

# جلب التوكن من متغيرات البيئة
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    print("📌 يرجى إضافة BOT_TOKEN في متغيرات البيئة في Railway")
    exit(1)

# ============= إزالة أي Webhook قديم =============
try:
    # إزالة webhook من API تليجرام مباشرة
    response = requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook')
    if response.status_code == 200:
        print("✅ تم حذف webhook بنجاح")
    else:
        print(f"⚠️ فشل حذف webhook: {response.text}")
except Exception as e:
    print(f"⚠️ خطأ في حذف webhook: {e}")

# ============= إنشاء البوت =============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# تعطيل الـ threading لمنع التعارضات
apihelper.ENABLE_MIDDLEWARE = False

# ============= تسجيل المعالجات =============
register_all_handlers(bot)

# ============= رسالة بدء التشغيل =============
print("=" * 60)
print("🤖 بوت الزخرفة والترجمة المتقدم")
print("=" * 60)
print(f"📌 التوكن: {TOKEN[:10]}...{TOKEN[-5:]}")
print(f"👑 قائمة الادمن: {os.environ.get('ADMIN_IDS', 'غير محددة')}")
print("=" * 60)

# الحصول على معلومات البوت
try:
    bot_info = bot.get_me()
    print(f"✅ البوت يعمل بنجاح!")
    print(f"🤖 اسم البوت: @{bot_info.username}")
    print(f"🆔 معرف البوت: {bot_info.id}")
except Exception as e:
    print(f"⚠️ خطأ في الاتصال بالبوت: {e}")
    print("📌 تأكد من صحة التوكن")

print("=" * 60)
print("📊 المميزات:")
print("   🎨 25+ خط عربي")
print("   🆎 11+ خط إنجليزي")
print("   🇰🇷 8+ ترجمة كورية")
print("   🇨🇳 8+ ترجمة صينية")
print("   𓂀 8+ ترجمة فرعونية")
print("   📝 200+ بايو لكل قسم")
print("   🎨 تأثيرات إضافية")
print("   👑 لوحة تحكم الادمن")
print("=" * 60)
print("🚀 بدء تشغيل البوت...")
print("=" * 60)

# ============= تشغيل البوت =============
if __name__ == "__main__":
    # استخدام polling مع إعادة محاولة قوية
    while True:
        try:
            # تشغيل البوت مع إعدادات مناسبة
            bot.polling(
                none_stop=True,           # لا تتوقف عند الأخطاء
                interval=0,               # لا انتظار بين الطلبات
                timeout=30,               # مهلة الطلب
                long_polling_timeout=30,  # مهلة الـ long polling
                allowed_updates=None,     # استقبل كل التحديثات
                skip_pending=False        # لا تتخطى التحديثات المعلقة
            )
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ خطأ في polling: {error_msg}")
            
            # إذا كان الخطأ 409، نعيد حذف webhook
            if "409" in error_msg or "Conflict" in error_msg:
                print("🔄 تم اكتشاف تعارض، جاري إعادة ضبط webhook...")
                try:
                    requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook')
                    print("✅ تم إعادة ضبط webhook")
                except:
                    pass
            
            print("🔄 إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)
