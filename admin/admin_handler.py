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
from .channels import ChannelsManager
from database.db_manager import Database

db = Database()

# ============= إعدادات الادمن =============

def get_admin_ids():
    """الحصول على قائمة الادمن من متغيرات البيئة"""
    admin_ids_str = os.environ.get('ADMIN_IDS', '')
    if admin_ids_str:
        return [int(id.strip()) for id in admin_ids_str.split(',') if id.strip().isdigit()]
    return []

ADMIN_IDS = get_admin_ids()

def is_admin(user_id):
    """التحقق من أن المستخدم أدمن"""
    return user_id in ADMIN_IDS

def get_admin_keyboard():
    """الحصول على كيبورد الادمن"""
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

def get_admin_info_text():
    """الحصول على نص معلومات الادمن"""
    admin_list = []
    for admin_id in ADMIN_IDS:
        admin_list.append(str(admin_id))
    
    total_users = db.get_user_count()
    active_today = db.get_active_users_today()
    new_today = db.get_new_users_today()
    required_channels = db.get_required_channels()
    
    return f"""
👑 **لوحة تحكم الادمن** 👑

📊 **إحصائيات سريعة:**
• 👥 إجمالي المستخدمين: `{total_users}`
• 🔥 نشط اليوم: `{active_today}`
• ✨ جدد اليوم: `{new_today}`

📢 **القنوات الإجبارية:** `{len(required_channels)}` قناة

👤 **المشرفون:** {', '.join(admin_list) if admin_list else 'لا يوجد'}

📌 **اختر الإجراء المناسب:**
    """

# ============= تسجيل معالجات الادمن =============

def register_admin_handlers(bot: TeleBot):
    
    # ============= أمر start مع ظهور أزرار الادمن =============
    @bot.message_handler(commands=['start', 'help'])
    def start_with_admin(message):
        """معالج start مع ظهور أزرار الادمن تلقائياً"""
        user_id = message.from_user.id
        
        welcome_text = """
✨ **بوت الزخرفة والترجمة المتقدم** ✨

📌 **اختر الخدمة التي تريدها من القائمة أدناه:**

• ✨ **زخرفة نصوص** - زخرفة الأسماء بخطوط عربية وإنجليزية فاخرة
• 🌍 **ترجمة الأسماء** - ترجمة إلى الكوري، الصيني، والفرعوني
• 📝 **بايوهات جاهزة** - بايوهات مميزة لواتساب، إنستجرام، ماسنجر
• 🎨 **تأثيرات إضافية** - خطوط تحت، وسط، نص مقلوب، وغيرها

✅ **جميع النصوص قابلة للنسخ بالضغط عليها مباشرة**
        """
        
        from keyboards.menus import main_menu
        
        # إذا كان المستخدم أدمن، أضف أزرار الادمن
        if is_admin(user_id):
            markup = main_menu()
            btn_admin = InlineKeyboardButton("👑 لوحة التحكم", callback_data="admin_panel")
            markup.add(btn_admin)
            bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=main_menu())
    
    # ============= أمر admin_info =============
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
    
    # ============= أمر admin (للخلفية) =============
    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        """أمر admin - يفتح لوحة التحكم"""
        if not is_admin(message.from_user.id):
            bot.send_message(
                message.chat.id,
                "⛔ **غير مصرح لك بدخول لوحة التحكم**\n\nهذه اللوحة مخصصة للمشرفين فقط.",
                parse_mode='Markdown'
            )
            return
        
        AdminPanel.show_main_panel(bot, message.chat.id)
    
    # ============= عرض لوحة التحكم =============
    @bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
    def show_admin_panel(call):
        """عرض لوحة التحكم"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        bot.edit_message_text(
            get_admin_info_text(),
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=get_admin_keyboard()
        )
        bot.answer_callback_query(call.id)
    
    # ============= معالج أزرار الادمن الرئيسية =============
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
        elif action == "channels":
            ChannelsManager.show_channels_panel(bot, call.message.chat.id, call.message.message_id)
        elif action == "back":
            AdminPanel.show_main_panel(bot, call.message.chat.id, call.message.message_id)
        
        bot.answer_callback_query(call.id)
    
    # ============= معالج أزرار البث =============
    @bot.callback_query_handler(func=lambda call: call.data.startswith("broadcast_"))
    def handle_broadcast_callbacks(call):
        """معالج أزرار البث"""
        from .broadcast import BroadcastManager
        
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        data_parts = call.data.split("_")
        
        if len(data_parts) < 3:
            bot.answer_callback_query(call.id, "⚠️ خطأ في البيانات", show_alert=True)
            return
        
        action = data_parts[1]
        
        if action == "target":
            if len(data_parts) < 4:
                bot.answer_callback_query(call.id, "⚠️ خطأ في البيانات", show_alert=True)
                return
            target = data_parts[2]
            chat_id = int(data_parts[3])
            BroadcastManager.send_broadcast(bot, chat_id, target)
            bot.answer_callback_query(call.id, f"🚀 جاري الإرسال إلى {target}...")
        
        elif action == "cancel":
            if len(data_parts) < 3:
                bot.answer_callback_query(call.id, "⚠️ خطأ في البيانات", show_alert=True)
                return
            chat_id = int(data_parts[2])
            BroadcastManager.cancel_broadcast(bot, chat_id)
            bot.answer_callback_query(call.id, "❌ تم الإلغاء")
    
    # ============= معالج أزرار القنوات =============
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_channel_"))
    def handle_channel_callbacks(call):
        """معالج أزرار القنوات"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        action = call.data.split("_")[2]
        
        if action == "add":
            ChannelsManager.add_channel(bot, call.message.chat.id)
            bot.answer_callback_query(call.id, "➕ أرسل معرف القناة")
        
        elif action == "remove":
            ChannelsManager.remove_channel(bot, call.message.chat.id)
            bot.answer_callback_query(call.id, "🗑️ اختر القناة للحذف")
        
        elif action == "test":
            ChannelsManager.test_channels(bot, call.message.chat.id)
            bot.answer_callback_query(call.id, "🔍 جاري اختبار القنوات...")
        
        elif action == "del":
            chat_id = call.data.split("_")[3]
            db.remove_required_channel(chat_id)
            bot.answer_callback_query(call.id, "✅ تم حذف القناة")
            ChannelsManager.show_channels_panel(bot, call.message.chat.id, call.message.message_id)
        
        elif action == "back":
            ChannelsManager.show_channels_panel(bot, call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id)
    
    # ============= معالج أزرار المستخدمين =============
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_user_"))
    def handle_user_callbacks(call):
        """معالج أزرار المستخدمين"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        action = call.data.split("_")[2]
        
        if action == "page":
            page = int(call.data.split("_")[3])
            UserManager.show_users_list(bot, call.message.chat.id, call.message.message_id, page)
            bot.answer_callback_query(call.id)
        
        elif action == "block":
            user_id = int(call.data.split("_")[3])
            db.block_user(user_id)
            bot.answer_callback_query(call.id, "🚫 تم حظر المستخدم")
            UserManager.show_users_list(bot, call.message.chat.id, call.message.message_id)
        
        elif action == "unblock":
            user_id = int(call.data.split("_")[3])
            db.unblock_user(user_id)
            bot.answer_callback_query(call.id, "✅ تم إلغاء حظر المستخدم")
            UserManager.show_users_list(bot, call.message.chat.id, call.message.message_id)
        
        elif action == "details":
            user_id = int(call.data.split("_")[3])
            UserManager.show_user_details(bot, call.message.chat.id, user_id)
            bot.answer_callback_query(call.id)
    
    # ============= معالج أزرار السجلات =============
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_logs_"))
    def handle_logs_callbacks(call):
        """معالج أزرار السجلات"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        action = call.data.split("_")[2]
        
        if action == "page":
            page = int(call.data.split("_")[3])
            LogsManager.show_logs(bot, call.message.chat.id, call.message.message_id, page)
            bot.answer_callback_query(call.id)
        
        elif action == "export":
            LogsManager.export_logs(bot, call.message.chat.id)
            bot.answer_callback_query(call.id, "📤 جاري تصدير السجلات...")
        
        elif action == "clear":
            db.clear_logs()
            bot.answer_callback_query(call.id, "🧹 تم مسح السجلات")
            LogsManager.show_logs(bot, call.message.chat.id, call.message.message_id)
    
    # ============= معالج أزرار التقارير =============
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_report_"))
    def handle_report_callbacks(call):
        """معالج أزرار التقارير"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        report_type = call.data.split("_")[2]
        
        if report_type == "daily":
            AdminPanel.show_daily_report(bot, call.message.chat.id, call.message.message_id)
        elif report_type == "weekly":
            AdminPanel.show_weekly_report(bot, call.message.chat.id, call.message.message_id)
        elif report_type == "monthly":
            AdminPanel.show_monthly_report(bot, call.message.chat.id, call.message.message_id)
        
        bot.answer_callback_query(call.id)
    
    # ============= معالج أزرار الإعدادات =============
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_setting_"))
    def handle_settings_callbacks(call):
        """معالج أزرار الإعدادات"""
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ غير مصرح لك", show_alert=True)
            return
        
        setting = call.data.split("_")[2]
        
        if setting == "welcome":
            SettingsManager.edit_welcome_message(bot, call.message.chat.id)
        elif setting == "admins":
            SettingsManager.manage_admins(bot, call.message.chat.id)
        elif setting == "limit":
            SettingsManager.edit_rate_limit(bot, call.message.chat.id)
        elif setting == "lang":
            SettingsManager.toggle_language(bot, call.message.chat.id)
        elif setting == "reset":
            SettingsManager.reset_settings(bot, call.message.chat.id)
        
        bot.answer_callback_query(call.id)