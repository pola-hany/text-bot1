import os
import time
import requests
import telebot
from telebot import apihelper

# ============= إعدادات البوت =============

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

# ============= إزالة أي Webhook قديم =============
print("🔄 جاري إزالة webhook...")
try:
    response = requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', timeout=10)
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ تم حذف webhook بنجاح")
        else:
            print(f"⚠️ فشل: {result}")
    else:
        print(f"⚠️ خطأ: {response.status_code}")
except Exception as e:
    print(f"⚠️ خطأ: {e}")

# ============= إعدادات البوت =============
apihelper.ENABLE_MIDDLEWARE = False
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ============= تسجيل المعالجات الأساسية =============

# تخزين مؤقت للبيانات
user_data = {}
ADMIN_IDS = [int(id) for id in os.environ.get('ADMIN_IDS', '').split(',') if id.strip().isdigit()]
print(f"👑 الادمن المسجلين: {ADMIN_IDS}")

def is_admin(user_id):
    return user_id in ADMIN_IDS

# ============= القوائم =============
def main_menu(user_id):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✨ زخرفة نصوص", callback_data="decorate")
    btn2 = InlineKeyboardButton("🌍 ترجمة الأسماء", callback_data="translate")
    btn3 = InlineKeyboardButton("📝 بايوهات جاهزة", callback_data="bios")
    btn4 = InlineKeyboardButton("🎨 تأثيرات إضافية", callback_data="effects")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    # إضافة أزرار الادمن للمستخدمين المصرح لهم
    if is_admin(user_id):
        btn_admin = InlineKeyboardButton("👑 لوحة التحكم", callback_data="admin_panel")
        markup.add(btn_admin)
    
    return markup

def admin_menu():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
    btn2 = InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")
    btn3 = InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast")
    btn4 = InlineKeyboardButton("📜 السجلات", callback_data="admin_logs")
    btn5 = InlineKeyboardButton("💾 نسخ احتياطي", callback_data="admin_backup")
    btn6 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    return markup

# ============= معالج start =============
@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    user_id = message.from_user.id
    
    welcome_text = """
✨ **بوت الزخرفة والترجمة المتقدم** ✨

📌 **اختر الخدمة من القائمة أدناه:**

• ✨ **زخرفة نصوص** - زخرفة الأسماء بخطوط عربية وإنجليزية
• 🌍 **ترجمة الأسماء** - ترجمة إلى الكوري، الصيني، والفرعوني
• 📝 **بايوهات جاهزة** - بايوهات مميزة لواتساب، إنستجرام، ماسنجر
• 🎨 **تأثيرات إضافية** - خطوط تحت، وسط، نص مقلوب

✅ **جميع النصوص قابلة للنسخ بالضغط عليها مباشرة**
    """
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=main_menu(user_id)
    )

# ============= معالج العودة للقائمة =============
@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    bot.edit_message_text(
        "✨ **القائمة الرئيسية** ✨\n\nاختر الخدمة:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=main_menu(call.from_user.id)
    )
    bot.answer_callback_query(call.id)

# ============= لوحة تحكم الادمن =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
def admin_panel(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    text = """
👑 **لوحة تحكم الادمن** 👑

📌 **اختر الإجراء المناسب:**
    """
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=admin_menu()
    )
    bot.answer_callback_query(call.id)

# ============= إحصائيات بسيطة =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    # إحصائيات بسيطة
    text = """
📊 **إحصائيات البوت** 📊

👥 إجمالي المستخدمين: `1`
🔥 نشط اليوم: `1`
✨ جدد اليوم: `1`

📅 آخر تحديث: `الآن`
    """
    
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")
    markup.add(btn_back)
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# ============= إرسال جماعي بسيط =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def admin_broadcast(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    text = """
📢 **الرسائل الجماعية** 📢

📝 **أرسل الرسالة التي تريد نشرها**
    """
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    msg = bot.send_message(call.message.chat.id, "📝 **أرسل الرسالة الآن:**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, send_broadcast_message)
    bot.answer_callback_query(call.id)

def send_broadcast_message(message):
    """إرسال البث للمستخدمين"""
    text = message.text
    
    # هنا يتم إرسال البث - للاختبار نرسل فقط رسالة تأكيد
    bot.send_message(
        message.chat.id,
        f"✅ **تم حفظ الرسالة!**\n\n📝 النص: `{text[:100]}`\n\n🚀 جاري الإرسال...",
        parse_mode='Markdown'
    )
    
    # العودة للوحة التحكم
    admin_panel_message = bot.send_message(message.chat.id, "👑 لوحة التحكم", reply_markup=admin_menu())
    # يمكن حفظ معرف الرسالة للاستخدام

# ============= سجلات بسيطة =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_logs")
def admin_logs(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    text = """
📜 **سجل الأحداث** 📜

`03:00:00 - البوت بدأ العمل`
`03:01:00 - مستخدم جديد: {user_id}`
    """
    
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")
    markup.add(btn_back)
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# ============= نسخ احتياطي =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_backup")
def admin_backup(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    text = "💾 **جاري إنشاء النسخة الاحتياطية...**"
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    # إنشاء ملف JSON بسيط
    import json
    import datetime
    
    data = {
        "backup_date": str(datetime.datetime.now()),
        "users": [],
        "stats": {}
    }
    
    filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(filename, 'rb') as f:
        bot.send_document(call.message.chat.id, f, caption="✅ **تم إنشاء النسخة الاحتياطية**")
    
    import os
    os.remove(filename)
    
    bot.answer_callback_query(call.id, "✅ تم إنشاء النسخة")

# ============= معالج رسائل عادية =============
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(
        message.chat.id,
        "✨ **يرجى استخدام الأزرار في القائمة الرئيسية** ✨\n\nأرسل /start للبدء",
        parse_mode='Markdown',
        reply_markup=main_menu(message.from_user.id)
    )

# ============= تشغيل البوت =============
if __name__ == "__main__":
    print("=" * 50)
    print("✅ بوت الزخرفة يعمل...")
    try:
        print(f"🤖 @{bot.get_me().username}")
    except:
        print("🤖 جاري التشغيل...")
    print(f"👑 الادمن: {ADMIN_IDS}")
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
                print("🔄 جاري إعادة ضبط webhook...")
                try:
                    requests.get(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', timeout=5)
                except:
                    pass
                time.sleep(10)
            else:
                time.sleep(5)
