from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class SettingsManager:
    
    @staticmethod
    def show_settings(bot: TeleBot, chat_id, message_id=None):
        settings = db.get_settings()
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn_welcome = InlineKeyboardButton("✏️ رسالة الترحيب", callback_data="admin_setting_welcome")
        btn_limit = InlineKeyboardButton("⏱️ حد الطلبات", callback_data="admin_setting_limit")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_welcome, btn_limit)
        markup.add(btn_back)
        
        text = f"""
⚙️ **إعدادات البوت**

📝 **الإعدادات الحالية:**
• حد الطلبات: `{settings.get('rate_limit', 30)}` طلب/دقيقة
• اللغة: `{settings.get('language', 'عربي')}`

📌 **اختر الإعداد لتعديله:**
        """
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)