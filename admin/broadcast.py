from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()
broadcast_messages = {}

class BroadcastManager:
    
    @staticmethod
    def show_broadcast_panel(bot: TeleBot, chat_id, message_id=None):
        markup = InlineKeyboardMarkup()
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_back)
        
        text = """
📢 **الرسائل الجماعية** 📢

📝 **أرسل الرسالة التي تريد نشرها**

✅ سيتم إرسالها لجميع المستخدمين
        """
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
        
        msg = bot.send_message(chat_id, "📝 **أرسل الرسالة الآن:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, BroadcastManager.process_broadcast)
    
    @staticmethod
    def process_broadcast(message):
        chat_id = message.chat.id
        text = message.text
        
        broadcast_messages[chat_id] = text
        
        markup = InlineKeyboardMarkup()
        btn_send = InlineKeyboardButton("🚀 إرسال", callback_data="broadcast_send")
        btn_cancel = InlineKeyboardButton("❌ إلغاء", callback_data="broadcast_cancel")
        markup.add(btn_send, btn_cancel)
        
        bot.send_message(
            chat_id,
            f"✅ **تم حفظ الرسالة!**\n\n📝 النص:\n`{text[:200]}`\n\n🚀 اضغط إرسال للنشر",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @staticmethod
    def send_broadcast(bot: TeleBot, chat_id):
        text = broadcast_messages.get(chat_id)
        if not text:
            bot.send_message(chat_id, "❌ **لا توجد رسالة**", parse_mode='Markdown')
            return
        
        users = db.get_all_users()
        total = len(users)
        success = 0
        failed = 0
        
        status_msg = bot.send_message(chat_id, f"🚀 جاري الإرسال إلى {total} مستخدم...")
        
        for user in users:
            try:
                user_id = user.get('user_id') or user.get('id')
                if isinstance(user_id, str) and user_id.isdigit():
                    user_id = int(user_id)
                bot.send_message(user_id, text, parse_mode='Markdown')
                success += 1
            except:
                failed += 1
        
        bot.edit_message_text(
            f"✅ **تم الانتهاء!**\n\n✅ نجح: {success}\n❌ فشل: {failed}",
            chat_id,
            status_msg.message_id,
            parse_mode='Markdown'
        )
        
        db.add_log(f"Broadcast sent to {success} users", "admin")
        
        if chat_id in broadcast_messages:
            del broadcast_messages[chat_id]