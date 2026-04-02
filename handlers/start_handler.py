from telebot import TeleBot
from keyboards.menus import main_menu_with_admin

def register_start_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['start', 'help'])
    def start_command(message):
        user_id = message.from_user.id
        
        welcome_text = """
✨ **بوت الزخرفة والترجمة المتقدم** ✨

📌 **اختر الخدمة من القائمة أدناه:**

• ✨ **زخرفة نصوص** - زخرفة الأسماء بخطوط عربية وإنجليزية
• 🌍 **ترجمة الأسماء** - ترجمة إلى الكوري، الصيني، والفرعوني
• 📝 **بايوهات جاهزة** - بايوهات مميزة لواتساب، إنستجرام، ماسنجر
• 🎨 **تأثيرات إضافية** - خطوط تحت، وسط، نص مقلوب

✅ **جميع النصوص قابلة للنسخ بالضغط عليها مباشرة**
        """
        
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='Markdown',
            reply_markup=main_menu_with_admin(user_id)
        )