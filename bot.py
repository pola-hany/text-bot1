import os
import time
import json
import requests
import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import apihelper

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
bot = TeleBot(TOKEN, parse_mode='HTML')

# ============= قاعدة بيانات بسيطة =============
DB_FILE = 'database.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'users': {}, 'stats': {}, 'required_channels': [], 'logs': []}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_db()

# ============= الادمن =============
ADMIN_IDS = [int(id) for id in os.environ.get('ADMIN_IDS', '').split(',') if id.strip().isdigit()]
print(f"👑 الادمن: {ADMIN_IDS}")

def is_admin(user_id):
    return user_id in ADMIN_IDS

# ============= إدارة المستخدمين =============
def add_user(user_id, username):
    user_id = str(user_id)
    if user_id not in db['users']:
        db['users'][user_id] = {
            'id': user_id,
            'username': username,
            'joined': str(datetime.datetime.now()),
            'last_active': str(datetime.datetime.now()),
            'requests': 0
        }
        save_db(db)
        return True
    return False

def update_user_activity(user_id):
    user_id = str(user_id)
    if user_id in db['users']:
        db['users'][user_id]['last_active'] = str(datetime.datetime.now())
        db['users'][user_id]['requests'] += 1
        save_db(db)

# ============= القنوات الإجبارية =============
def get_required_channels():
    return db.get('required_channels', [])

def add_required_channel(chat_id, username, name):
    channels = db.get('required_channels', [])
    # تحقق من عدم التكرار
    for ch in channels:
        if ch['chat_id'] == chat_id:
            return False
    channels.append({
        'chat_id': chat_id,
        'username': username,
        'name': name
    })
    db['required_channels'] = channels
    save_db(db)
    return True

def remove_required_channel(chat_id):
    channels = db.get('required_channels', [])
    channels = [ch for ch in channels if ch['chat_id'] != chat_id]
    db['required_channels'] = channels
    save_db(db)
    return True

# ============= السجلات =============
def add_log(action, user="system"):
    db['logs'].append({
        'time': str(datetime.datetime.now()),
        'action': action,
        'user': user
    })
    if len(db['logs']) > 100:
        db['logs'] = db['logs'][-100:]
    save_db(db)

# ============= القوائم =============
def main_menu(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✨ زخرفة نصوص", callback_data="decorate")
    btn2 = InlineKeyboardButton("🌍 ترجمة الأسماء", callback_data="translate")
    btn3 = InlineKeyboardButton("📝 بايوهات جاهزة", callback_data="bios")
    btn4 = InlineKeyboardButton("🎨 تأثيرات إضافية", callback_data="effects")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    if is_admin(user_id):
        btn_admin = InlineKeyboardButton("👑 لوحة التحكم", callback_data="admin_panel")
        markup.add(btn_admin)
    
    return markup

def admin_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
    btn2 = InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")
    btn3 = InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast")
    btn4 = InlineKeyboardButton("📜 السجلات", callback_data="admin_logs")
    btn5 = InlineKeyboardButton("💾 نسخ احتياطي", callback_data="admin_backup")
    btn6 = InlineKeyboardButton("📢 القنوات الإجبارية", callback_data="admin_channels")
    btn7 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)
    return markup

def channels_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("➕ إضافة قناة", callback_data="admin_channel_add")
    btn2 = InlineKeyboardButton("➖ حذف قناة", callback_data="admin_channel_remove")
    btn3 = InlineKeyboardButton("🔍 اختبار القنوات", callback_data="admin_channel_test")
    btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup

# ============= معالج start =============
@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    add_user(user_id, username)
    update_user_activity(user_id)
    
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

# ============= العودة للقائمة =============
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
    
    total_users = len(db['users'])
    active_today = sum(1 for u in db['users'].values() if u.get('last_active', '').startswith(str(datetime.date.today())))
    channels_count = len(get_required_channels())
    
    text = f"""
👑 **لوحة تحكم الادمن** 👑

📊 **إحصائيات سريعة:**
• 👥 إجمالي المستخدمين: `{total_users}`
• 🔥 نشط اليوم: `{active_today}`
• 📢 القنوات الإجبارية: `{channels_count}`

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

# ============= الإحصائيات =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    total_users = len(db['users'])
    active_today = sum(1 for u in db['users'].values() if u.get('last_active', '').startswith(str(datetime.date.today())))
    total_requests = sum(u.get('requests', 0) for u in db['users'].values())
    
    text = f"""
📊 **إحصائيات البوت** 📊

👥 **المستخدمين:**
• إجمالي: `{total_users}`
• نشط اليوم: `{active_today}`

📈 **الطلبات:**
• إجمالي الطلبات: `{total_requests}`
• متوسط الطلبات: `{total_requests // max(total_users, 1)}`

📅 آخر تحديث: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}`
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

# ============= إدارة المستخدمين =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def admin_users(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    users = list(db['users'].values())[-10:]  # آخر 10 مستخدمين
    
    text = "👥 **قائمة المستخدمين** (آخر 10)\n\n"
    for i, user in enumerate(users, 1):
        text += f"{i}. `{user['id']}` | @{user.get('username', 'لا يوجد')}\n"
        text += f"   📅 {user.get('joined', '')[:10]} | {user.get('requests', 0)} طلب\n\n"
    
    if not users:
        text += "⚠️ لا يوجد مستخدمين بعد\n"
    
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

# ============= إرسال جماعي =============
broadcast_message = {}

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def admin_broadcast(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    bot.edit_message_text(
        "📢 **الرسائل الجماعية** 📢\n\n📝 **أرسل الرسالة التي تريد نشرها**",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    msg = bot.send_message(call.message.chat.id, "📝 **أرسل الرسالة الآن:**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_broadcast)
    bot.answer_callback_query(call.id)

def process_broadcast(message):
    chat_id = message.chat.id
    text = message.text
    
    broadcast_message[chat_id] = text
    
    markup = InlineKeyboardMarkup()
    btn_all = InlineKeyboardButton("📢 لجميع المستخدمين", callback_data="broadcast_send_all")
    btn_cancel = InlineKeyboardButton("❌ إلغاء", callback_data="broadcast_cancel")
    markup.add(btn_all)
    markup.add(btn_cancel)
    
    bot.send_message(
        chat_id,
        f"✅ **تم حفظ الرسالة!**\n\n📝 النص:\n`{text[:200]}`\n\n🎯 **اختر المستهدفين:**",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "broadcast_send_all")
def send_broadcast(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    text = broadcast_message.get(call.message.chat.id)
    if not text:
        bot.answer_callback_query(call.id, "⚠️ لا توجد رسالة", show_alert=True)
        return
    
    users = db['users'].values()
    total = len(users)
    success = 0
    failed = 0
    
    status_msg = bot.send_message(call.message.chat.id, f"🚀 جاري الإرسال إلى {total} مستخدم...")
    
    for user in users:
        try:
            bot.send_message(int(user['id']), text, parse_mode='Markdown')
            success += 1
        except:
            failed += 1
    
    bot.edit_message_text(
        f"✅ **تم الانتهاء!**\n\n✅ نجح: {success}\n❌ فشل: {failed}",
        call.message.chat.id,
        status_msg.message_id,
        parse_mode='Markdown'
    )
    
    add_log(f"Broadcast sent to {success} users", str(call.from_user.id))
    bot.answer_callback_query(call.id, "✅ تم الإرسال")

@bot.callback_query_handler(func=lambda call: call.data == "broadcast_cancel")
def cancel_broadcast(call):
    if call.message.chat.id in broadcast_message:
        del broadcast_message[call.message.chat.id]
    bot.edit_message_text("❌ **تم إلغاء البث**", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
    bot.answer_callback_query(call.id)

# ============= السجلات =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_logs")
def admin_logs(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    logs = db['logs'][-20:]  # آخر 20 سجل
    
    text = "📜 **سجل الأحداث** (آخر 20)\n\n"
    for log in reversed(logs):
        text += f"`{log['time'][:16]}` | [{log['user']}] {log['action'][:50]}\n"
    
    if not logs:
        text += "⚠️ لا توجد سجلات بعد\n"
    
    markup = InlineKeyboardMarkup()
    btn_clear = InlineKeyboardButton("🧹 مسح السجلات", callback_data="admin_logs_clear")
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel")
    markup.add(btn_clear)
    markup.add(btn_back)
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_logs_clear")
def clear_logs(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    db['logs'] = []
    save_db(db)
    bot.answer_callback_query(call.id, "🧹 تم مسح السجلات")
    admin_logs(call)

# ============= نسخ احتياطي =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_backup")
def admin_backup(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    bot.edit_message_text(
        "💾 **جاري إنشاء النسخة الاحتياطية...**",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    with open(filename, 'rb') as f:
        bot.send_document(call.message.chat.id, f, caption="✅ **تم إنشاء النسخة الاحتياطية**")
    
    os.remove(filename)
    add_log("Backup created", str(call.from_user.id))
    bot.answer_callback_query(call.id, "✅ تم الإنشاء")

# ============= إدارة القنوات الإجبارية =============
@bot.callback_query_handler(func=lambda call: call.data == "admin_channels")
def admin_channels(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    channels = get_required_channels()
    
    text = "📢 **إدارة القنوات الإجبارية**\n\n"
    
    if channels:
        text += "**القنوات الحالية:**\n"
        for i, ch in enumerate(channels, 1):
            text += f"{i}. {ch['name']} (@{ch['username']})\n"
    else:
        text += "⚠️ لا توجد قنوات إجبارية\n\n"
    
    text += "\n📌 **المستخدمون لن يتمكنوا من استخدام البوت إلا بعد الاشتراك في هذه القنوات**"
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=channels_menu()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "admin_channel_add")
def add_channel(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    bot.edit_message_text(
        "➕ **إضافة قناة جديدة**\n\n"
        "📌 **أرسل معرف القناة:**\n"
        "• بالصيغة: `@username`\n"
        "• أو المعرف الرقمي: `-100123456789`\n\n"
        "❌ لإلغاء العملية أرسل `cancel`",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )
    
    msg = bot.send_message(call.message.chat.id, "📝 **أرسل معرف القناة:**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_add_channel)
    bot.answer_callback_query(call.id)

def process_add_channel(message):
    chat_id = message.chat.id
    channel_input = message.text.strip()
    
    if channel_input.lower() == 'cancel':
        bot.send_message(chat_id, "❌ **تم إلغاء الإضافة**", parse_mode='Markdown')
        admin_panel_message = bot.send_message(chat_id, "👑 لوحة التحكم", reply_markup=admin_menu())
        return
    
    try:
        # محاولة الحصول على معلومات القناة
        channel_username = channel_input.replace('@', '')
        chat = bot.get_chat(channel_input)
        channel_name = chat.title if chat.title else channel_username
        
        add_required_channel(str(chat.id), channel_username, channel_name)
        
        bot.send_message(
            chat_id,
            f"✅ **تم إضافة القناة بنجاح!**\n\n"
            f"📢 الاسم: {channel_name}\n"
            f"🆔 المعرف: @{channel_username}",
            parse_mode='Markdown'
        )
        add_log(f"Added channel: {channel_name}", str(message.from_user.id))
        
    except Exception as e:
        bot.send_message(
            chat_id,
            f"❌ **فشل إضافة القناة!**\n\n⚠️ الخطأ: {str(e)}\n\n"
            f"📌 تأكد من:\n"
            f"• صحة معرف القناة\n"
            f"• البوت أدمن في القناة",
            parse_mode='Markdown'
        )
    
    admin_panel_message = bot.send_message(chat_id, "👑 لوحة التحكم", reply_markup=admin_menu())

@bot.callback_query_handler(func=lambda call: call.data == "admin_channel_remove")
def remove_channel(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    channels = get_required_channels()
    
    if not channels:
        bot.answer_callback_query(call.id, "⚠️ لا توجد قنوات للحذف", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in channels:
        btn = InlineKeyboardButton(f"❌ {ch['name']}", callback_data=f"channel_del_{ch['chat_id']}")
        markup.add(btn)
    
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_channels")
    markup.add(btn_back)
    
    bot.edit_message_text(
        "🗑️ **اختر القناة للحذف:**",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("channel_del_"))
def delete_channel(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    chat_id = call.data.split("_")[2]
    remove_required_channel(chat_id)
    
    bot.answer_callback_query(call.id, "✅ تم حذف القناة")
    admin_channels(call)

@bot.callback_query_handler(func=lambda call: call.data == "admin_channel_test")
def test_channels(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
        return
    
    channels = get_required_channels()
    
    if not channels:
        bot.answer_callback_query(call.id, "⚠️ لا توجد قنوات للاختبار", show_alert=True)
        return
    
    text = "🔍 **نتيجة اختبار القنوات:**\n\n"
    all_ok = True
    
    for ch in channels:
        try:
            bot.get_chat_member(ch['chat_id'], bot.get_me().id)
            text += f"✅ {ch['name']} - يعمل\n"
        except Exception as e:
            text += f"❌ {ch['name']} - خطأ: {str(e)[:50]}\n"
            all_ok = False
    
    if all_ok:
        text += "\n✨ **جميع القنوات تعمل بشكل صحيح!**"
    else:
        text += "\n⚠️ **يرجى التأكد من أن البوت أدمن في القنوات المذكورة**"
    
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_channels")
    markup.add(btn_back)
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

# ============= معالجات الخدمات الأخرى =============
@bot.callback_query_handler(func=lambda call: call.data == "decorate")
def decorate_service(call):
    bot.answer_callback_query(call.id, "✨ قريباً...")
    bot.send_message(call.message.chat.id, "✨ **خدمة الزخرفة** قريباً ستصبح متاحة!", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "translate")
def translate_service(call):
    bot.answer_callback_query(call.id, "🌍 قريباً...")
    bot.send_message(call.message.chat.id, "🌍 **خدمة الترجمة** قريباً ستصبح متاحة!", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "bios")
def bios_service(call):
    bot.answer_callback_query(call.id, "📝 قريباً...")
    bot.send_message(call.message.chat.id, "📝 **خدمة البايوهات** قريباً ستصبح متاحة!", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "effects")
def effects_service(call):
    bot.answer_callback_query(call.id, "🎨 قريباً...")
    bot.send_message(call.message.chat.id, "🎨 **خدمة التأثيرات** قريباً ستصبح متاحة!", parse_mode='Markdown')

# ============= معالج الرسائل العادية =============
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
    print(f"📢 القنوات الإجبارية: {len(get_required_channels())}")
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
