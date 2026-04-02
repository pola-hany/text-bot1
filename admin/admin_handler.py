import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_ids():
    admin_ids_str = os.environ.get('ADMIN_IDS', '')
    if admin_ids_str:
        return [int(id.strip()) for id in admin_ids_str.split(',') if id.strip().isdigit()]
    return []

ADMIN_IDS = get_admin_ids()

def is_admin(user_id):
    return user_id in ADMIN_IDS

def register_admin_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        if not is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ غير مصرح لك", parse_mode='Markdown')
            return
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
        btn2 = InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")
        btn3 = InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast")
        btn4 = InlineKeyboardButton("📜 السجلات", callback_data="admin_logs")
        btn5 = InlineKeyboardButton("💾 نسخ احتياطي", callback_data="admin_backup")
        btn6 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        
        bot.send_message(message.chat.id, "👑 **لوحة تحكم الادمن**", parse_mode='Markdown', reply_markup=markup)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def handle_admin(call):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        action = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"🚀 جاري تنفيذ {action}")
        bot.send_message(call.message.chat.id, f"✨ أمر **{action}** سيتم تفعيله قريباً", parse_mode='Markdown')