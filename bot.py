import os
import time
import requests
import telebot
from telebot import apihelper
from handlers import register_all_handlers
from database.db_manager import Database
from admin.admin_handler import is_admin, get_admin_ids

# ============= إعدادات البوت =============

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

# ============= قاعدة البيانات =============
db = Database()

# ============= دالة التحقق من الاشتراك =============
def check_subscription(user_id):
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
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    markup = InlineKeyboardMarkup(row_width=1)
    for channel in db.get_required_channels():
        btn = InlineKeyboardButton(f"📢 {channel['name']}", url=f"https://t.me/{channel['username']}")
        markup.add(btn)
    btn_check = InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription")
    markup.add(btn_check)
    return markup

# ============= معالج التحقق =============
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق! مرحباً بك")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        from keyboards.menus import main_menu
        bot.send_message(
            call.message.chat.id,
            "✨ **مرحباً بك في البوت!** ✨\n\n📌 يمكنك الآن استخدام جميع الخدمات.",
            parse_mode='Markdown',
            reply_markup=main_menu(call.from_user.id)
        )
    else:
        bot.answer_callback_query(call.id, "❌ يرجى الاشتراك في جميع القنوات أولاً", show_alert=True)

# ============= معالج الوسيط =============
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    allowed_commands = ['/start', '/help', '/admin', '/admin_info']
    
    if message.text and message.text.startswith('/'):
        if message.text in allowed_commands:
            bot.process_new_messages([message])
            return
    
    if not check_subscription(message.from_user.id):
        text = "🔒 **للوصول إلى البوت، يرجى الاشتراك في القنوات التالية:**\n\n"
        for channel in db.get_required_channels():
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
    
    bot.process_new_messages([message])

# ============= تسجيل جميع المعالجات من الملفات الموجودة =============
register_all_handlers(bot)

# ============= تشغيل البوت =============
if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة يعمل...")
    try:
        print(f"🤖 @{bot.get_me().username}")
    except:
        print("🤖 جاري التشغيل...")
    print(f"👑 الادمن: {get_admin_ids()}")
    print(f"📢 القنوات الإجبارية: {len(db.get_required_channels())}")
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
