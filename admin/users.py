from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class UserManager:
    
    @staticmethod
    def show_users_list(bot, chat_id, message_id=None, page=0):
        """عرض قائمة المستخدمين"""
        users_per_page = 10
        users = db.get_all_users(limit=users_per_page, offset=page * users_per_page)
        total_users = db.get_user_count()
        total_pages = (total_users + users_per_page - 1) // users_per_page
        
        text = f"👥 **قائمة المستخدمين** (الصفحة {page + 1}/{total_pages})\n\n"
        
        for i, user in enumerate(users, 1):
            status = "🟢 نشط" if user.get('active', True) else "🔴 محظور"
            text += f"{i}. `{user['user_id']}` | {user.get('username', 'لا يوجد')}\n"
            text += f"   📅 {user.get('joined_date', 'غير معروف')} | {status}\n"
            text += f"   📊 {user.get('requests', 0)} طلب\n\n"
        
        markup = InlineKeyboardMarkup(row_width=2)
        
        if page > 0:
            btn_prev = InlineKeyboardButton("⬅️ السابق", callback_data=f"admin_users_page_{page-1}")
            markup.add(btn_prev)
        if page < total_pages - 1:
            btn_next = InlineKeyboardButton("التالي ➡️", callback_data=f"admin_users_page_{page+1}")
            markup.add(btn_next)
        
        btn_search = InlineKeyboardButton("🔍 بحث", callback_data="admin_users_search")
        btn_export = InlineKeyboardButton("📤 تصدير", callback_data="admin_export_users")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_search, btn_export)
        markup.add(btn_back)
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def show_user_details(bot, chat_id, user_id):
        """عرض تفاصيل مستخدم"""
        user = db.get_user(user_id)
        
        text = f"""
👤 **معلومات المستخدم**

🆔 المعرف: `{user['user_id']}`
👤 اليوزر: @{user.get('username', 'لا يوجد')}
📅 تاريخ الانضمام: `{user.get('joined_date', 'غير معروف')}`
🕐 آخر نشاط: `{user.get('last_active', 'غير معروف')}`
📊 عدد الطلبات: `{user.get('requests', 0)}`
✅ الحالة: `{'نشط' if user.get('active', True) else 'محظور'}`

🎨 **الخدمات المستخدمة:**
• زخرفة: {user.get('decoration_count', 0)} مرة
• ترجمة: {user.get('translation_count', 0)} مرة
• بايوهات: {user.get('bios_count', 0)} مرة
• تأثيرات: {user.get('effects_count', 0)} مرة
        """
        
        markup = InlineKeyboardMarkup()
        if user.get('active', True):
            btn_block = InlineKeyboardButton("🚫 حظر المستخدم", callback_data=f"admin_block_user_{user_id}")
            markup.add(btn_block)
        else:
            btn_unblock = InlineKeyboardButton("✅ إلغاء الحظر", callback_data=f"admin_unblock_user_{user_id}")
            markup.add(btn_unblock)
        
        btn_msg = InlineKeyboardButton("💬 إرسال رسالة", callback_data=f"admin_msg_user_{user_id}")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_users")
        markup.add(btn_msg)
        markup.add(btn_back)
        
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)