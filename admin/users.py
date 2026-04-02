from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class UserManager:
    
    @staticmethod
    def show_users_list(bot: TeleBot, chat_id, message_id=None, page=0):
        users_per_page = 10
        users = db.get_all_users(limit=users_per_page, offset=page * users_per_page)
        total_users = len(db.get_all_users())
        total_pages = (total_users + users_per_page - 1) // users_per_page if total_users > 0 else 1
        
        text = f"👥 **قائمة المستخدمين** (الصفحة {page + 1}/{total_pages})\n\n"
        
        for i, user in enumerate(users, 1):
            user_id = user.get('user_id') or user.get('id', '?')
            username = user.get('username', 'لا يوجد')
            joined = user.get('joined_date') or user.get('joined', '')
            requests_count = user.get('requests', 0)
            text += f"{i}. `{str(user_id)[:15]}` | @{username}\n"
            text += f"   📅 {joined[:10]} | 📊 {requests_count} طلب\n\n"
        
        if not users:
            text += "⚠️ لا يوجد مستخدمين بعد\n"
        
        markup = InlineKeyboardMarkup(row_width=2)
        
        if page > 0:
            btn_prev = InlineKeyboardButton("⬅️ السابق", callback_data=f"admin_users_page_{page-1}")
            markup.add(btn_prev)
        if page < total_pages - 1:
            btn_next = InlineKeyboardButton("التالي ➡️", callback_data=f"admin_users_page_{page+1}")
            markup.add(btn_next)
        
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_back)
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)