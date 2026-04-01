from datetime import datetime, timedelta
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class StatsManager:
    
    @staticmethod
    def show_stats(bot, chat_id, message_id=None):
        """عرض الإحصائيات"""
        # إحصائيات أساسية
        total_users = db.get_user_count()
        active_today = db.get_active_users_today()
        active_week = db.get_active_users_week()
        new_today = db.get_new_users_today()
        new_week = db.get_new_users_week()
        new_month = db.get_new_users_month()
        
        # إحصائيات الخدمات
        service_stats = db.get_service_stats()
        
        # أوقات الذروة
        peak_hours = db.get_peak_hours()
        
        text = f"""
📊 **إحصائيات البوت** 📊

👥 **المستخدمين:**
• إجمالي: `{total_users}`
• نشط اليوم: `{active_today}`
• نشط الأسبوع: `{active_week}`
• جدد اليوم: `{new_today}`
• جدد الأسبوع: `{new_week}`
• جدد الشهر: `{new_month}`

🎨 **الخدمات:**
• زخرفة: `{service_stats.get('decoration', 0)}` طلب
• ترجمة: `{service_stats.get('translation', 0)}` طلب
• بايوهات: `{service_stats.get('bios', 0)}` طلب
• تأثيرات: `{service_stats.get('effects', 0)}` طلب

⏰ **أوقات الذروة:**
{peak_hours}

📈 **متوسط الطلبات اليومية:** `{db.get_daily_avg()}`
💾 **حجم قاعدة البيانات:** `{db.get_db_size()}`

📅 آخر تحديث: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
        """
        
        markup = InlineKeyboardMarkup()
        btn_refresh = InlineKeyboardButton("🔄 تحديث", callback_data="admin_stats")
        btn_export = InlineKeyboardButton("📤 تصدير", callback_data="admin_export_stats")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_refresh)
        markup.add(btn_export, btn_back)
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)