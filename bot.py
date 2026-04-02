import os
import time
import requests
import telebot
from telebot import apihelper
from handlers import register_all_handlers
from database.db_manager import Database

# ============= إعدادات البوت =============

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

# ============= إزالة أي Webhook قديم =============
print("🔄 جاري إزالة webhook القديم...")
try:
    response = requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', timeout=10)
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ تم حذف webhook بنجاح")
        else:
            print(f"⚠️ فشل حذف webhook: {result}")
    else:
        print(f"⚠️ خطأ في الاتصال: {response.status_code}")
except Exception as e:
    print(f"⚠️ خطأ في حذف webhook: {e}")

# ============= إعدادات خاصة لمنع 409 =============
# تعطيل الـ threading نهائياً
apihelper.ENABLE_MIDDLEWARE = False

# إنشاء البوت
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ============= قاعدة البيانات =============
db = Database()

# ============= دالة التحقق من الاشتراك =============
def check_subscription(user_id):
    """التحقق من اشتراك المستخدم في القنوات الإجبارية"""
    required_channels = db.get_required_channels()
    
    if not required_channels:
        return True
    
    for channel in required_channels:
        try:
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

# ============= تسجيل المعالجات =============
register_all_handlers(bot)

# ============= معالج التحقق من الاشتراك =============
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    """معالج التحقق من الاشتراك"""
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق! مرحباً بك")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        from keyboards.menus import main_menu
        bot.send_message(
            call.message.chat.id,
            "✨ **مرحباً بك في البوت!** ✨\n\n"
            "📌 يمكنك الآن استخدام جميع الخدمات.",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
    else:
        bot.answer_callback_query(call.id, "❌ يرجى الاشتراك في جميع القنوات أولاً", show_alert=True)

# ============= معالج الوسيط للتحقق من الاشتراك =============
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """معالج عام للرسائل مع التحقق من الاشتراك"""
    # الأوامر المسموح بها بدون اشتراك
    allowed_commands = ['/start', '/help', '/admin', '/admin_info']
    
    if message.text and message.text.startswith('/'):
        if message.text in allowed_commands:
            # تمرير للمعالجات الأخرى
            bot.process_new_messages([message])
            return
    
    if not check_subscription(message.from_user.id):
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
print(f"👑 الادمن: {os.environ.get('ADMIN_IDS', 'غير محدد')}")
print("=" * 60)

try:
    bot_info = bot.get_me()
    print(f"✅ البوت يعمل بنجاح!")
    print(f"🤖 @{bot_info.username}")
    print(f"🆔 ID: {bot_info.id}")
except Exception as e:
    print(f"⚠️ خطأ: {e}")

print("=" * 60)
print("📊 المميزات:")
print("   🎨 25+ خط عربي")
print("   🆎 11+ خط إنجليزي")
print("   🇰🇷 8+ ترجمة كورية")
print("   🇨🇳 8+ ترجمة صينية")
print("   𓂀 8+ ترجمة فرعونية")
print("   📝 200+ بايو")
print("   🎨 تأثيرات")
print("   👑 لوحة ادمن")
print("   🔒 اشتراك إجباري")
print("=" * 60)
print("🚀 بدء التشغيل...")
print("=" * 60)

# ============= تشغيل البوت =============
if __name__ == "__main__":
    while True:
        try:
            # استخدام polling بدون threading
            bot.polling(
                none_stop=True,
                interval=1,
                timeout=30,
                long_polling_timeout=30,
                allowed_updates=None,
                skip_pending=True
            )
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ خطأ: {error_msg}")
            
            if "409" in error_msg or "Conflict" in error_msg:
                print("🔄 جاري إعادة ضبط webhook...")
                try:
                    requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', timeout=5)
                    print("✅ تم إعادة ضبط webhook")
                except:
                    pass
                
                # انتظار أطول قبل إعادة المحاولة
                time.sleep(10)
            else:
                time.sleep(5)
