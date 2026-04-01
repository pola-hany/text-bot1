import json
from datetime import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database
from .admin_handler import ADMIN_IDS

db = Database()

class AdminPanel:
    
    @staticmethod
    def show_main_panel(bot, chat_id, message_id=None):
        """عرض لوحة التحكم الرئيسية"""
        markup = InlineKeyboardMarkup(row_width=2)
        
        # صفوف الأزرار
        btn_stats = InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")
        btn_users = InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")
        btn_broadcast = InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast")
        btn_settings = InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")
        btn_logs = InlineKeyboardButton("📜 السجلات", callback_data="admin_logs")
        btn_backup = InlineKeyboardButton("💾 نسخ احتياطي", callback_data="admin_backup")
        btn_reports = InlineKeyboardButton("📈 تقارير", callback_data="admin_reports")
        btn_security = InlineKeyboardButton("🛡️ الحماية", callback_data="admin_security")
        
        markup.add(btn_stats, btn_users)
        markup.add(btn_broadcast, btn_settings)
        markup.add(btn_logs, btn_backup)
        markup.add(btn_reports, btn_security)
        
        # إحصائيات سريعة
        total_users = db.get_user_count()
        active_today = db.get_active_users_today()
        new_today = db.get_new_users_today()
        
        # معلومات الادمن
        admin_list = []
        for admin_id in ADMIN_IDS:
            user = db.get_user(admin_id)
            if user:
                admin_list.append(f"@{user.get('username', str(admin_id))}")
            else:
                admin_list.append(str(admin_id))
        
        admins_text = ", ".join(admin_list) if admin_list else "لا يوجد"
        
        text = f"""
👑 **لوحة تحكم الادمن** 👑

📊 **إحصائيات سريعة:**
• 👥 إجمالي المستخدمين: `{total_users}`
• 🔥 نشط اليوم: `{active_today}`
• ✨ جدد اليوم: `{new_today}`

👤 **المشرفون:**
{admins_text}

📌 **اختر الإجراء المناسب:**
        """
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def backup_data(bot, chat_id, message_id=None):
        """نسخ احتياطي للبيانات"""
        data = db.get_all_data()
        
        # حفظ في ملف JSON
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # إرسال الملف
        with open(filename, 'rb') as f:
            bot.send_document(chat_id, f, caption=f"💾 **نسخة احتياطية**\n📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        import os
        os.remove(filename)
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_back"))
        
        text = "✅ **تم إنشاء النسخة الاحتياطية وإرسالها**"
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def show_reports(bot, chat_id, message_id=None):
        """عرض التقارير"""
        markup = InlineKeyboardMarkup(row_width=2)
        btn_daily = InlineKeyboardButton("📅 تقرير يومي", callback_data="admin_report_daily")
        btn_weekly = InlineKeyboardButton("📊 تقرير أسبوعي", callback_data="admin_report_weekly")
        btn_monthly = InlineKeyboardButton("📈 تقرير شهري", callback_data="admin_report_monthly")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_daily, btn_weekly)
        markup.add(btn_monthly)
        markup.add(btn_back)
        
        text = "📊 **لوحة التقارير**\n\nاختر نوع التقرير:"
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def show_security(bot, chat_id, message_id=None):
        """عرض إعدادات الحماية"""
        markup = InlineKeyboardMarkup(row_width=2)
        btn_blocked = InlineKeyboardButton("🚫 المستخدمين المحظورين", callback_data="admin_blocked_users")
        btn_rate_limit = InlineKeyboardButton("⏱️ حد الطلبات", callback_data="admin_rate_limit")
        btn_antispam = InlineKeyboardButton("🛡️ مكافحة السبام", callback_data="admin_antispam")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_blocked, btn_rate_limit)
        markup.add(btn_antispam)
        markup.add(btn_back)
        
        text = "🛡️ **لوحة الحماية**\n\nإعدادات الأمان والحماية:"
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)