import json
import datetime
import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database
from .admin_handler import get_admin_keyboard

db = Database()

class AdminPanel:
    
    @staticmethod
    def show_main_panel(bot: TeleBot, chat_id, message_id=None):
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
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=get_admin_keyboard())
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=get_admin_keyboard())
    
    @staticmethod
    def backup_data(bot: TeleBot, chat_id, message_id=None):
        data = db.get_all_data()
        filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        with open(filename, 'rb') as f:
            bot.send_document(chat_id, f, caption="✅ **تم إنشاء النسخة الاحتياطية**")
        
        os.remove(filename)
        db.add_log("Backup created", "admin")
        
        if message_id:
            bot.edit_message_text("✅ تم إنشاء النسخة الاحتياطية", chat_id, message_id, parse_mode='Markdown')