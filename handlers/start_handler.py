from telebot import TeleBot

def register_start_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(
            message.chat.id,
            "✨ **بوت الزخرفة المتقدم** ✨\n\n"
            "📌 **أرسل اسمك أو أي نص**\n"
            "📌 **اختر نوع الزخرفة**\n"
            "📌 **اضغط على أي نص للنسخ المباشر**\n\n"
            "🎯 **أرسل النص الآن:**",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(message, save_name)
    
    def save_name(message):
        from handlers.decoration_handler import save_user_name
        save_user_name(bot, message)