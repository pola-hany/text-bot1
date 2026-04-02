from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class ChannelsManager:
    
    @staticmethod
    def show_channels_panel(bot: TeleBot, chat_id, message_id=None):
        channels = db.get_required_channels()
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn_add = InlineKeyboardButton("➕ إضافة قناة", callback_data="admin_channel_add")
        btn_remove = InlineKeyboardButton("➖ حذف قناة", callback_data="admin_channel_remove")
        btn_test = InlineKeyboardButton("🔍 اختبار القنوات", callback_data="admin_channel_test")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn_add, btn_remove)
        markup.add(btn_test)
        markup.add(btn_back)
        
        text = "📢 **إدارة القنوات الإجبارية**\n\n"
        
        if channels:
            text += "**القنوات الحالية:**\n"
            for i, ch in enumerate(channels, 1):
                text += f"{i}. {ch['name']} (@{ch['username']})\n"
        else:
            text += "⚠️ لا توجد قنوات إجبارية\n\n"
        
        text += "\n📌 **المستخدمون لن يتمكنوا من استخدام البوت إلا بعد الاشتراك في هذه القنوات**"
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def add_channel(bot: TeleBot, chat_id):
        msg = bot.send_message(
            chat_id,
            "➕ **إضافة قناة جديدة**\n\n"
            "📌 **أرسل معرف القناة:**\n"
            "• بالصيغة: `@username`\n"
            "• أو المعرف الرقمي: `-100123456789`\n\n"
            "❌ لإلغاء العملية أرسل `cancel`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, ChannelsManager.process_add_channel)
    
    @staticmethod
    def process_add_channel(message):
        chat_id = message.chat.id
        channel_input = message.text.strip()
        
        if channel_input.lower() == 'cancel':
            bot.send_message(chat_id, "❌ **تم إلغاء الإضافة**", parse_mode='Markdown')
            return
        
        try:
            channel_username = channel_input.replace('@', '')
            chat = bot.get_chat(channel_input)
            channel_name = chat.title if chat.title else channel_username
            
            db.add_required_channel(str(chat.id), channel_username, channel_name)
            
            bot.send_message(
                chat_id,
                f"✅ **تم إضافة القناة بنجاح!**\n\n"
                f"📢 الاسم: {channel_name}\n"
                f"🆔 المعرف: @{channel_username}",
                parse_mode='Markdown'
            )
            db.add_log(f"Added channel: {channel_name}", "admin")
            
        except Exception as e:
            bot.send_message(
                chat_id,
                f"❌ **فشل إضافة القناة!**\n\n⚠️ الخطأ: {str(e)}\n\n"
                f"📌 تأكد من:\n"
                f"• صحة معرف القناة\n"
                f"• البوت أدمن في القناة",
                parse_mode='Markdown'
            )
    
    @staticmethod
    def remove_channel(bot: TeleBot, chat_id):
        channels = db.get_required_channels()
        
        if not channels:
            bot.send_message(chat_id, "⚠️ لا توجد قنوات للحذف", parse_mode='Markdown')
            return
        
        markup = InlineKeyboardMarkup(row_width=1)
        for ch in channels:
            btn = InlineKeyboardButton(f"❌ {ch['name']}", callback_data=f"channel_del_{ch['chat_id']}")
            markup.add(btn)
        
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_channels")
        markup.add(btn_back)
        
        bot.send_message(chat_id, "🗑️ **اختر القناة للحذف:**", parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def test_channels(bot: TeleBot, chat_id):
        channels = db.get_required_channels()
        
        if not channels:
            bot.send_message(chat_id, "⚠️ لا توجد قنوات للاختبار", parse_mode='Markdown')
            return
        
        text = "🔍 **نتيجة اختبار القنوات:**\n\n"
        
        for ch in channels:
            try:
                bot.get_chat_member(ch['chat_id'], bot.get_me().id)
                text += f"✅ {ch['name']} - يعمل\n"
            except Exception as e:
                text += f"❌ {ch['name']} - خطأ: {str(e)[:50]}\n"
        
        markup = InlineKeyboardMarkup()
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_channels")
        markup.add(btn_back)
        
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)