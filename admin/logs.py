from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class LogsManager:
    
    @staticmethod
    def show_logs(bot: TeleBot, chat_id, message_id=None, page=0):
        logs_per_page = 10
        logs = db.get_logs(limit=logs_per_page, offset=page * logs_per_page)
        total_logs = db.get_logs_count()
        total_pages = (total_logs + logs_per_page - 1) // logs_per_page if total_logs > 0 else 1
        
        text = f"📜 **سجل الأحداث** (الصفحة {page + 1}/{total_pages})\n\n"
        
        for log in logs:
            time = log.get('time', '')[:16]
            action = log.get('action', '')
            user = log.get('user', 'system')
            text += f"`{time}` | [{user}] {action[:50]}\n"
        
        if not logs:
            text += "⚠️ لا توجد سجلات بعد\n"
        
        markup = InlineKeyboardMarkup(row_width=2)
        
        if page > 0:
            btn_prev = InlineKeyboardButton("⬅️ السابق", callback_data=f"admin_logs_page_{page-1}")
            markup.add(btn_prev)
        if page < total_pages - 1:
            btn_next = InlineKeyboardButton("التالي ➡️", callback_data=f"admin_logs_page_{page+1}")
            markup.add(btn_next)
        
        btn_clear = InlineKeyboardButton("🧹 مسح السجلات", callback_data="admin_logs_clear")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_clear)
        markup.add(btn_back)
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)