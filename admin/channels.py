from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()

class ChannelsManager:
    
    @staticmethod
    def show_channels_panel(bot, chat_id, message_id=None):
        """عرض لوحة إدارة القنوات الإجبارية"""
        required_channels = db.get_required_channels()
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn_add = InlineKeyboardButton("➕ إضافة قناة", callback_data="admin_channel_add")
        btn_remove = InlineKeyboardButton("➖ حذف قناة", callback_data="admin_channel_remove")
        btn_test = InlineKeyboardButton("🔍 اختبار القنوات", callback_data="admin_channel_test")
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        
        markup.add(btn_add, btn_remove)
        markup.add(btn_test)
        markup.add(btn_back)
        
        text = "📢 **إدارة القنوات الإجبارية**\n\n"
        
        if required_channels:
            text += "**القنوات الحالية:**\n"
            for i, channel in enumerate(required_channels, 1):
                text += f"{i}. {channel['name']} (@{channel['username']})\n"
                text += f"   🆔 المعرف: `{channel['chat_id']}`\n\n"
        else:
            text += "⚠️ **لا توجد قنوات إجبارية حالياً**\n\n"
        
        text += "📌 **ملاحظة:** المستخدمون لن يتمكنوا من استخدام البوت إلا بعد الاشتراك في هذه القنوات."
        
        if message_id:
            bot.edit_message_text(text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    @staticmethod
    def add_channel(bot, chat_id):
        """إضافة قناة جديدة"""
        msg = bot.send_message(
            chat_id,
            "📢 **إضافة قناة جديدة**\n\n"
            "📌 **أرسل معرف القناة بالصيغة التالية:**\n"
            "`@username` أو `-100123456789`\n\n"
            "📝 **مثال:**\n"
            "`@my_channel`\n"
            "أو\n"
            "`-100123456789`\n\n"
            "❌ لإلغاء العملية أرسل `cancel`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, lambda m: ChannelsManager.process_add_channel(bot, m))
    
    @staticmethod
    def process_add_channel(bot, message):
        """معالجة إضافة القناة"""
        chat_id = message.chat.id
        channel_input = message.text.strip()
        
        if channel_input.lower() == 'cancel':
            bot.send_message(chat_id, "❌ **تم إلغاء الإضافة**", parse_mode='Markdown')
            ChannelsManager.show_channels_panel(bot, chat_id)
            return
        
        # استخراج معرف القناة
        channel_id = channel_input
        username = channel_input
        
        if channel_input.startswith('@'):
            username = channel_input[1:]
        elif channel_input.startswith('-100'):
            channel_id = int(channel_input)
            username = str(channel_id)
        
        try:
            # محاولة الحصول على معلومات القناة
            chat = bot.get_chat(channel_input)
            channel_name = chat.title if chat.title else username
            
            # حفظ القناة
            db.add_required_channel({
                'chat_id': str(chat.id),
                'username': username,
                'name': channel_name
            })
            
            bot.send_message(
                chat_id,
                f"✅ **تم إضافة القناة بنجاح!**\n\n"
                f"📢 الاسم: {channel_name}\n"
                f"🆔 المعرف: @{username}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            bot.send_message(
                chat_id,
                f"❌ **فشل إضافة القناة!**\n\n"
                f"⚠️ الخطأ: {str(e)}\n\n"
                f"📌 تأكد من:\n"
                f"• صحة معرف القناة\n"
                f"• البوت أدمن في القناة",
                parse_mode='Markdown'
            )
        
        ChannelsManager.show_channels_panel(bot, chat_id)
    
    @staticmethod
    def remove_channel(bot, chat_id):
        """حذف قناة"""
        required_channels = db.get_required_channels()
        
        if not required_channels:
            bot.send_message(chat_id, "⚠️ **لا توجد قنوات للحذف**", parse_mode='Markdown')
            ChannelsManager.show_channels_panel(bot, chat_id)
            return
        
        markup = InlineKeyboardMarkup(row_width=1)
        for channel in required_channels:
            btn = InlineKeyboardButton(
                f"❌ {channel['name']}", 
                callback_data=f"admin_channel_del_{channel['chat_id']}"
            )
            markup.add(btn)
        
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_channels")
        markup.add(btn_back)
        
        bot.send_message(
            chat_id,
            "🗑️ **اختر القناة للحذف:**",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @staticmethod
    def test_channels(bot, chat_id):
        """اختبار عمل القنوات"""
        required_channels = db.get_required_channels()
        
        if not required_channels:
            bot.send_message(chat_id, "⚠️ **لا توجد قنوات للاختبار**", parse_mode='Markdown')
            ChannelsManager.show_channels_panel(bot, chat_id)
            return
        
        text = "🔍 **نتيجة اختبار القنوات:**\n\n"
        all_ok = True
        
        for channel in required_channels:
            try:
                bot.get_chat_member(channel['chat_id'], bot.get_me().id)
                text += f"✅ {channel['name']} - يعمل\n"
            except Exception as e:
                text += f"❌ {channel['name']} - خطأ: {str(e)[:50]}\n"
                all_ok = False
        
        if all_ok:
            text += "\n✨ **جميع القنوات تعمل بشكل صحيح!**"
        else:
            text += "\n⚠️ **يرجى التأكد من أن البوت أدمن في القنوات المذكورة أعلاه**"
        
        markup = InlineKeyboardMarkup()
        btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="admin_channels")
        markup.add(btn_back)
        
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)