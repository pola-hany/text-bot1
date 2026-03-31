import random
from telebot import TeleBot
from keyboards.menus import main_menu
from fonts.arabic_fonts import ARABIC_FONTS
from fonts.english_fonts import ENGLISH_FONTS

# تخزين الأسماء مؤقتاً
user_names = {}

def save_user_name(bot: TeleBot, message):
    """حفظ اسم المستخدم"""
    user_names[message.chat.id] = message.text
    bot.send_message(
        message.chat.id,
        f"✅ تم استلام: **{message.text}**\n\n"
        f"🎨 **اختر نوع الزخرفة:**",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

def send_decorations(bot: TeleBot, chat_id, name, lang):
    """إرسال الزخارف كل واحدة في رسالة منفصلة"""
    fonts = ARABIC_FONTS if lang == "arabic" else ENGLISH_FONTS
    selected = random.sample(fonts, min(8, len(fonts)))
    
    for font in selected:
        try:
            decorated_text = font["func"](name)
            text = f"{font['emoji']} **{font['name']}**\n`{decorated_text}`\n_{font['desc']}_"
            
            bot.send_message(
                chat_id,
                text,
                parse_mode='Markdown',
                reply_markup=None
            )
        except Exception as e:
            continue
    
    # إرسال أزرار التحكم
    from keyboards.menus import get_more_button
    bot.send_message(
        chat_id,
        "🎯 **للحصول على المزيد من الزخارف:**",
        parse_mode='Markdown',
        reply_markup=get_more_button(name, lang)
    )

def register_decoration_handlers(bot: TeleBot):
    
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        """أي رسالة غير أوامر تعتبر اسم جديد"""
        save_user_name(bot, message)
    
    def get_user_name(chat_id):
        return user_names.get(chat_id, "")
    
    # إضافة الدوال للاستخدام في callback
    bot.get_user_name = get_user_name
    bot.user_names = user_names