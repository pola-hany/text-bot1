import os
import json
from datetime import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .admin_panel import AdminPanel
from .stats import StatsManager
from .users import UserManager
from .broadcast import BroadcastManager
from .settings import SettingsManager
from .logs import LogsManager

# جلب قائمة الادمن من متغيرات البيئة
def get_admin_ids():
    """الحصول على قائمة الادمن من متغيرات البيئة"""
    admin_ids_str = os.environ.get('ADMIN_IDS', '')
    if admin_ids_str:
        # تنسيق: 123456789,987654321,555555555
        return [int(id.strip()) for id in admin_ids_str.split(',') if id.strip().isdigit()]
    return []

ADMIN_IDS = get_admin_ids()

def is_admin(user_id):
    """التحقق من أن المستخدم أدمن"""
    return user_id in ADMIN_IDS

def register_admin_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        """لوحة تحكم الادمن"""
        user_id = message.from_user.id
        
        print(f"👑 محاولة دخول لوحة التحكم من: {user_id}")
        print(f"📋 قائمة الادمن: {ADMIN_IDS}")
        
        if not is_admin(user_id):
            bot.send_message(
                message.chat.id,
                "⛔ **غير مصرح لك بدخول لوحة التحكم**\n\nهذه اللوحة مخصصة للمشرفين فقط.\n\n"
                f"👤 معرفك: `{user_id}`\n"
                f"👥 الادمن المسموح لهم: `{ADMIN_IDS if ADMIN_IDS else 'لا يوجد'}`",
                parse_mode='Markdown'
            )
            return
        
        bot.send_message(
            message.chat.id,
            "👑 **جاري فتح لوحة التحكم...**",
            parse_mode='Markdown'
        )
        
        AdminPanel.show_main_panel(bot, message.chat.id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def handle_admin_callbacks(call):
        """معالج أزرار لوحة التحكم"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        action = call.data.split("_")[1]
        
        if action == "stats":
            StatsManager.show_stats(bot, call.message.chat.id, call.message.message_id)
        elif action == "users":
            UserManager.show_users_list(bot, call.message.chat.id, call.message.message_id)
        elif action == "broadcast":
            BroadcastManager.show_broadcast_panel(bot, call.message.chat.id, call.message.message_id)
        elif action == "settings":
            SettingsManager.show_settings(bot, call.message.chat.id, call.message.message_id)
        elif action == "logs":
            LogsManager.show_logs(bot, call.message.chat.id, call.message.message_id)
        elif action == "backup":
            AdminPanel.backup_data(bot, call.message.chat.id, call.message.message_id)
        elif action == "reports":
            AdminPanel.show_reports(bot, call.message.chat.id, call.message.message_id)
        elif action == "security":
            AdminPanel.show_security(bot, call.message.chat.id, call.message.message_id)
        elif action == "back":
            AdminPanel.show_main_panel(bot, call.message.chat.id, call.message.message_id)
        
        bot.answer_callback_query(call.id)
    
    # أمر لطباعة معلومات الادمن للتأكد
    @bot.message_handler(commands=['admin_info'])
    def admin_info(message):
        """عرض معلومات الادمن"""
        user_id = message.from_user.id
        is_admin_user = is_admin(user_id)
        
        text = f"""
👑 **معلومات الادمن**

👤 معرفك: `{user_id}`
🔐 هل أنت أدمن: `{is_admin_user}`

👥 قائمة الادمن المسجلين:
"""
        if ADMIN_IDS:
            for admin_id in ADMIN_IDS:
                text += f"• `{admin_id}`\n"
        else:
            text += "• لا يوجد ادمن مسجلين\n"
        
        text += f"""
📌 **لتصبح أدمن:**
1. احصل على معرفك من @userinfobot
2. أضف المعرف في متغير ADMIN_IDS في Railway
3. أعد تشغيل البوت
"""
        
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
