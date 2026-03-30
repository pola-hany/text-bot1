import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fonts.arabic_fonts import arabic_fonts
from fonts.english_fonts import english_fonts

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# تخزين مؤقت
user_data = {}  # {chat_id: {'lang': 'arabic/english', 'name': 'text'}}

# ============= الأزرار =============

def language_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🇸🇦 عربي - 50 خط", callback_data="lang_arabic")
    btn2 = InlineKeyboardButton("🇬🇧 English - 50 Fonts", callback_data="lang_english")
    markup.add(btn1, btn2)
    return markup

def get_action_menu(name, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_{lang}_{name}")
    btn2 = InlineKeyboardButton("🔄 اسم جديد", callback_data="new_name")
    btn3 = InlineKeyboardButton("🔙 تغيير اللغة", callback_data="change_lang")
    markup.add(btn1)
    markup.add(btn2, btn3)
    return markup

def get_random_fonts(name, lang, count=10):
    """جلب خطوط عشوائية مع إيموجي مناسب"""
    fonts = arabic_fonts if lang == 'arabic' else english_fonts
    selected = random.sample(fonts, min(count, len(fonts)))
    
    results = []
    for font in selected:
        # تطبيق الخط على الاسم
        converted = font['func'](name)
        # إضافة الإيموجي المناسب
        results.append(f"{font['emoji']} {converted}")
    
    return results

# ============= أوامر البوت =============

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
🌟 **بوت الزخرفة المتقدم - 50 خط لكل لغة** 🌟

✨ **المميزات:**
• 50 خط مختلف للغة العربية
• 50 خط مختلف للغة الإنجليزية
• كل خط مع إيموجي مناسب
• نسخ مباشر بالضغط على النص

📌 **اختر اللغة أولاً:**
"""
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=language_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.message.chat.id
    
    if call.data == "lang_arabic":
        user_data[user_id] = {'lang': 'arabic', 'name': None}
        bot.edit_message_text(
            "🇸🇦 **تم اختيار العربية - 50 خط** 🇸🇦\n\n📝 **أرسل الاسم أو النص:**",
            user_id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(call.message, save_name)
        bot.answer_callback_query(call.id)
    
    elif call.data == "lang_english":
        user_data[user_id] = {'lang': 'english', 'name': None}
        bot.edit_message_text(
            "🇬🇧 **English Selected - 50 Fonts** 🇬🇧\n\n📝 **Send your name or text:**",
            user_id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(call.message, save_name)
        bot.answer_callback_query(call.id)
    
    elif call.data == "change_lang":
        bot.edit_message_text(
            "🌍 **اختر اللغة:**",
            user_id,
            call.message.message_id,
            reply_markup=language_menu()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "new_name":
        lang = user_data.get(user_id, {}).get('lang', 'arabic')
        lang_text = "عربي" if lang == 'arabic' else "English"
        bot.edit_message_text(
            f"📝 **أرسل الاسم الجديد** ({lang_text}):",
            user_id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(call.message, save_name)
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith("more_"):
        parts = call.data.split("_", 2)
        lang = parts[1]
        name = parts[2]
        
        fonts = get_random_fonts(name, lang, 10)
        title = "🇸🇦 **المزيد من الخطوط العربية** 🇸🇦\n\n" if lang == 'arabic' else "🇬🇧 **More English Fonts** 🇬🇧\n\n"
        response = title + "\n\n".join(fonts)
        
        bot.edit_message_text(
            response,
            user_id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_action_menu(name, lang)
        )
        bot.answer_callback_query(call.id)

def save_name(message):
    user_id = message.chat.id
    name = message.text
    lang = user_data.get(user_id, {}).get('lang', 'arabic')
    
    user_data[user_id]['name'] = name
    
    fonts = get_random_fonts(name, lang, 10)
    
    title = "🇸🇦 **خطوط عربية - 50 خط** 🇸🇦\n\n" if lang == 'arabic' else "🇬🇧 **English Fonts - 50 Styles** 🇬🇧\n\n"
    response = title + "\n\n".join(fonts)
    
    bot.send_message(
        user_id,
        response,
        parse_mode='HTML',
        reply_markup=get_action_menu(name, lang)
    )

if __name__ == "__main__":
    print("✅ بوت الخطوط المتقدم يعمل...")
    print(f"🤖 @{bot.get_me().username}")
    print(f"📊 عدد الخطوط العربية: {len(arabic_fonts)}")
    print(f"📊 عدد الخطوط الإنجليزية: {len(english_fonts)}")
    bot.infinity_polling()