import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============= الادمن =============
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
    btn_stats = InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
    btn_users = InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")
    btn_broadcast = InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast")
    btn_settings = InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")
    btn_logs = InlineKeyboardButton("📜 السجلات", callback_data="admin_logs")
    btn_backup = InlineKeyboardButton("💾 نسخ احتياطي", callback_data="admin_backup")
    btn_reports = InlineKeyboardButton("📈 تقارير", callback_data="admin_reports")
    btn_security = InlineKeyboardButton("🛡️ الحماية", callback_data="admin_security")
    btn_channels = InlineKeyboardButton("📢 القنوات الإجبارية", callback_data="admin_channels")
    
    markup.add(btn_stats, btn_users)
    markup.add(btn_broadcast, btn_settings)
    markup.add(btn_logs, btn_backup)
    markup.add(btn_reports, btn_security)
    markup.add(btn_channels)
    return markup

def register_admin_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['admin', 'admin_panel'])
    def admin_command(message):
        if not is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "⛔ غير مصرح لك", parse_mode='Markdown')
            return
        
        from .admin_panel import AdminPanel
        AdminPanel.show_main_panel(bot, message.chat.id)
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
    def admin_panel_callback(call):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        from .admin_panel import AdminPanel
        AdminPanel.show_main_panel(bot, call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    
    # باقي المعالجات بنفس الطريقة
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
        elif action == "logs":
            from .logs import LogsManager
            LogsManager.show_logs(bot, call.message.chat.id, call.message.message_id)
        elif action == "backup":
            from .admin_panel import AdminPanel
            AdminPanel.backup_data(bot, call.message.chat.id, call.message.message_id)
        elif action == "channels":
            from .channels import ChannelsManager
            ChannelsManager.show_channels_panel(bot, call.message.chat.id, call.message.message_id)
        elif action == "back":
            from .admin_panel import AdminPanel
            AdminPanel.show_main_panel(bot, call.message.chat.id, call.message.message_id)
        
        bot.answer_callback_query(call.id)