import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fonts.arabic_fonts import ARABIC_FONTS
from fonts.english_fonts import ENGLISH_FONTS
from database.db_manager import Database

db = Database()
user_texts = {}

def register_decoration_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "decorate")
    def decorate_callback(call):
        bot.answer_callback_query(call.id, "✨ أرسل النص للزخرفة")
        msg = bot.send_message(
            call.message.chat.id,
            "✨ **أرسل النص أو الاسم الذي تريد زخرفته:**",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, ask_decoration_lang)
    
    def ask_decoration_lang(message):
        user_texts[message.chat.id] = message.text
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("🇸🇦 زخرفة عربية", callback_data=f"deco_arabic_{message.chat.id}")
        btn2 = InlineKeyboardButton("🇬🇧 زخرفة إنجليزية", callback_data=f"deco_english_{message.chat.id}")
        markup.add(btn1, btn2)
        
        bot.send_message(
            message.chat.id,
            f"✅ تم استلام: **{message.text}**\n\n🎨 **اختر نوع الزخرفة:**",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("deco_"))
    def handle_decoration(call):
        parts = call.data.split("_")
        lang = parts[1]
        user_id = int(parts[2])
        text = user_texts.get(user_id, "")
        
        if not text:
            bot.answer_callback_query(call.id, "⚠️ يرجى إرسال النص أولاً", show_alert=True)
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        if lang == "arabic":
            send_arabic_decorations(bot, call.message.chat.id, text)
        else:
            send_english_decorations(bot, call.message.chat.id, text)
        
        db.update_user_activity(call.from_user.id, "decoration")
        bot.answer_callback_query(call.id, "✨ جاري توليد الزخارف...")

def send_arabic_decorations(bot, chat_id, text):
    selected = random.sample(ARABIC_FONTS, min(10, len(ARABIC_FONTS)))
    
    for font in selected:
        try:
            decorated = font["func"](text)
            msg = f"{font['emoji']} **{font['name']}**\n`{decorated}`\n_{font['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_deco_arabic")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="decorate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(chat_id, "🎯 **للحصول على المزيد من الزخارف:**", parse_mode='Markdown', reply_markup=markup)

def send_english_decorations(bot, chat_id, text):
    selected = random.sample(ENGLISH_FONTS, min(10, len(ENGLISH_FONTS)))
    
    for font in selected:
        try:
            decorated = font["func"](text)
            msg = f"{font['emoji']} **{font['name']}**\n`{decorated}`\n_{font['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_deco_english")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="decorate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(chat_id, "🎯 **للحصول على المزيد من الزخارف:**", parse_mode='Markdown', reply_markup=markup)