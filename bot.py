import os
import time
import requests
import telebot
from telebot import apihelper
from handlers import register_all_handlers
from database.db_manager import Database

# ============= إعدادات البوت =============

# جلب التوكن من متغيرات البيئة
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    print("📌 يرجى إضافة BOT_TOKEN في متغيرات البيئة في Railway")
    exit(1)

# ============= إزالة أي Webhook قديم =============
try:
    response = requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook')
    if response.status_code == 200:
        print("✅ تم حذف webhook بنجاح")
except Exception as e:
    print(f"⚠️ خطأ في حذف webhook: {e}")

# ============= إنشاء البوت =============
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
apihelper.ENABLE_MIDDLEWARE = False

# ============= قاعدة البيانات =============
db = Database()

# ============= تسجيل المعالجات =============
register_all_handlers(bot)

# ============= دالة التحقق من الاشتراك =============
def check_subscription(user_id):
    """التحقق من اشتراك المستخدم في القنوات الإجبارية"""
    required_channels = db.get_required_channels()
    
    if not required_channels:
        return True
    
    for channel in required_channels:
        try:
            # التحقق من عضوية المستخدم
            chat_member = bot.get_chat_member(channel['chat_id'], user_id)
            if chat_member.status in ['left', 'kicked']:
                return False
        except:
            return False
    
    return True

def get_subscription_keyboard():
    """الحصول على كيبورد الاشتراك الإجباري"""
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    required_channels = db.get_required_channels()
    markup = InlineKeyboardMarkup(row_width=1)
    
    for channel in required_channels:
        btn = InlineKeyboardButton(
            f"📢 {channel['name']}", 
            url=f"https://t.me/{channel['username']}"
        )
        markup.add(btn)
    
    btn_check = InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription")
    markup.add(btn_check)
    
    return markup

# ============= معالج التحقق من الاشتراك =============
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    """معالج التحقق من الاشتراك"""
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق! مرحباً بك")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "✨ **مرحباً بك في البوت!** ✨\n\n"
            "📌 يمكنك الآن استخدام جميع الخدمات.\n"
            "📌 أرسل /start للبدء",
            parse_mode='Markdown'
        )
    else:
        bot.answer_callback_query(call.id, "❌ يرجى الاشتراك في جميع القنوات أولاً", show_alert=True)

# ============= معالج الوسيط للتحقق من الاشتراك =============
def subscription_middleware(message):
    """وسيط للتحقق من الاشتراك قبل أي أمر"""
    if message.text and message.text.startswith('/'):
        # الأوامر المسموح بها بدون اشتراك
        allowed_commands = ['/start', '/help', '/admin', '/admin_info']
        if message.text in allowed_commands:
            return True
    
    return check_subscription(message.from_user.id)

# ============= تعديل معالج الرسائل للتحقق =============
original_handlers = []

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_messages(message):
    """معالج عام للرسائل مع التحقق من الاشتراك"""
    if not check_subscription(message.from_user.id):
        # عرض رسالة الاشتراك الإجباري
        required_channels = db.get_required_channels()
        text = "🔒 **للوصول إلى البوت، يرجى الاشتراك في القنوات التالية:**\n\n"
        
        for channel in required_channels:
            text += f"• [{channel['name']}](https://t.me/{channel['username']})\n"
        
        text += "\n✅ بعد الاشتراك، اضغط على زر التحقق"
        
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_subscription_keyboard(),
            disable_web_page_preview=True
        )
        return
    
    # تمرير الرسالة للمعالجات الأخرى
    bot.process_new_messages([message])

# ============= رسالة بدء التشغيل =============
print("=" * 60)
print("🤖 بوت الزخرفة والترجمة المتقدم")
print("=" * 60)
print(f"📌 التوكن: {TOKEN[:10]}...{TOKEN[-5:]}")
print(f"👑 قائمة الادمن: {os.environ.get('ADMIN_IDS', 'غير محددة')}")
print("=" * 60)

try:
    bot_info = bot.get_me()
    print(f"✅ البوت يعمل بنجاح!")
    print(f"🤖 اسم البوت: @{bot_info.username}")
    print(f"🆔 معرف البوت: {bot_info.id}")
except Exception as e:
    print(f"⚠️ خطأ في الاتصال بالبوت: {e}")

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
print("   🔒 نظام اشتراك إجباري")
print("=" * 60)
print("🚀 بدء تشغيل البوت...")
print("=" * 60)

# ============= تشغيل البوت =============
if __name__ == "__main__":
    while True:
        try:
            bot.polling(
                none_stop=True,
                interval=0,
                timeout=30,
                long_polling_timeout=30,
                allowed_updates=None,
                skip_pending=False
            )
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ خطأ في polling: {error_msg}")
            
            if "409" in error_msg or "Conflict" in error_msg:
                print("🔄 تم اكتشاف تعارض، جاري إعادة ضبط webhook...")
                try:
                    requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook')
                    print("✅ تم إعادة ضبط webhook")
                except:
                    pass
            
            print("🔄 إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)