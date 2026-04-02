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

def get_admin_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
    btn2 = InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")
    btn3 = InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast")
    btn4 = InlineKeyboardButton("📢 القنوات الإجبارية", callback_data="admin_channels")
    btn5 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    return markup

def register_admin_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        if not is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ غير مصرح لك", parse_mode='Markdown')
            return
        
        from database.db_manager import Database
        db = Database()
        
        total_users = len(db.get_all_users())
        active_today = db.get_active_users_today()
        channels_count = len(db.get_required_channels())
        
        text = f"""
👑 **لوحة تحكم الادمن** 👑

📊 **إحصائيات سريعة:**
• 👥 إجمالي المستخدمين: `{total_users}`
• 🔥 نشط اليوم: `{active_today}`
• 📢 القنوات الإجبارية: `{channels_count}`

📌 **اختر الإجراء المناسب:**
        """
        
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_admin_keyboard())
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def handle_admin(call):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        action = call.data.split("_")[1]
        
        if action == "stats":
            from .stats import StatsManager
            StatsManager.show_stats(bot, call.message.chat.id, call.message.message_id)
        elif action == "users":
            from .users import UserManager
            UserManager.show_users_list(bot, call.message.chat.id, call.message.message_id)
        elif action == "broadcast":
            from .broadcast import BroadcastManager
            BroadcastManager.show_broadcast_panel(bot, call.message.chat.id, call.message.message_id)
        elif action == "channels":
            from .channels import ChannelsManager
            ChannelsManager.show_channels_panel(bot, call.message.chat.id, call.message.message_id)
        
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_back")
    def admin_back(call):
        from .admin_handler import get_admin_keyboard
        from database.db_manager import Database
        db = Database()
        
        total_users = len(db.get_all_users())
        active_today = db.get_active_users_today()
        channels_count = len(db.get_required_channels())
        
        text = f"""
👑 **لوحة تحكم الادمن** 👑

📊 **إحصائيات سريعة:**
• 👥 إجمالي المستخدمين: `{total_users}`
• 🔥 نشط اليوم: `{active_today}`
• 📢 القنوات الإجبارية: `{channels_count}`

📌 **اختر الإجراء المناسب:**
        """
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=get_admin_keyboard())
        bot.answer_callback_query(call.id)