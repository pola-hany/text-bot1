from telebot import TeleBot
from keyboards.menus import main_menu

def register_start_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        bot.send_message(
            message.chat.id,
            "✨ **بوت الزخرفة والترجمة المتقدم** ✨\n\n"
            "📌 **اختر الخدمة التي تريدها من القائمة:**\n\n"
            "• ✨ **زخرفة نصوص** - زخرفة الأسماء بخطوط عربية وإنجليزية فاخرة\n"
            "• 🌍 **ترجمة الأسماء** - ترجمة إلى الكوري، الصيني، والفرعوني\n"
            "• 📝 **بايوهات جاهزة** - بايوهات مميزة لواتساب، إنستجرام، ماسنجر\n"
            "• 🎨 **تأثيرات إضافية** - خطوط تحت، وسط، نص مقلوب، وغيرها\n\n"
            "✅ **جميع النصوص قابلة للنسخ بالضغط عليها مباشرة**",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )