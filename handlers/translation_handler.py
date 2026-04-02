import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fonts.korean_fonts import KOREAN_STYLES
from fonts.chinese_fonts import CHINESE_STYLES
from fonts.egyptian_fonts import EGYPTIAN_STYLES
from database.db_manager import Database

db = Database()
user_texts = {}

def register_translation_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "translate")
    def translate_callback(call):
        bot.answer_callback_query(call.id, "🌍 أرسل النص للترجمة")
        msg = bot.send_message(
            call.message.chat.id,
            "🌍 **أرسل الاسم أو النص للترجمة:**\n\n📌 يمكنك إرسال نص عربي أو إنجليزي",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, ask_translation_lang)
    
    def ask_translation_lang(message):
        user_texts[message.chat.id] = message.text
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("🇰🇷 كوري", callback_data=f"trans_korean_{message.chat.id}")
        btn2 = InlineKeyboardButton("🇨🇳 صيني", callback_data=f"trans_chinese_{message.chat.id}")
        btn3 = InlineKeyboardButton("𓂀 فرعوني", callback_data=f"trans_egyptian_{message.chat.id}")
        markup.add(btn1, btn2, btn3)
        
        bot.send_message(
            message.chat.id,
            f"✅ تم استلام: **{message.text}**\n\n🌍 **اختر لغة الترجمة:**",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("trans_"))
    def handle_translation(call):
        parts = call.data.split("_")
        lang = parts[1]
        user_id = int(parts[2])
        text = user_texts.get(user_id, "")
        
        if not text:
            bot.answer_callback_query(call.id, "⚠️ يرجى إرسال النص أولاً", show_alert=True)
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        if lang == "korean":
            send_korean_translations(bot, call.message.chat.id, text)
        elif lang == "chinese":
            send_chinese_translations(bot, call.message.chat.id, text)
        else:
            send_egyptian_translations(bot, call.message.chat.id, text)
        
        db.update_user_activity(call.from_user.id, "translation")
        bot.answer_callback_query(call.id, "✨ جاري الترجمة...")

def send_korean_translations(bot, chat_id, text):
    selected = random.sample(KOREAN_STYLES, min(8, len(KOREAN_STYLES)))
    for style in selected:
        try:
            translated = style["func"](text)
            msg = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data="translate")
    btn2 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    bot.send_message(chat_id, "🇰🇷 **للحصول على المزيد:**", parse_mode='Markdown', reply_markup=markup)

def send_chinese_translations(bot, chat_id, text):
    selected = random.sample(CHINESE_STYLES, min(8, len(CHINESE_STYLES)))
    for style in selected:
        try:
            translated = style["func"](text)
            msg = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data="translate")
    btn2 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    bot.send_message(chat_id, "🇨🇳 **للحصول على المزيد:**", parse_mode='Markdown', reply_markup=markup)

def send_egyptian_translations(bot, chat_id, text):
    selected = random.sample(EGYPTIAN_STYLES, min(8, len(EGYPTIAN_STYLES)))
    for style in selected:
        try:
            translated = style["func"](text)
            msg = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data="translate")
    btn2 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
    markup.add(btn1, btn2)
    bot.send_message(chat_id, "𓂀 **للحصول على المزيد:**", parse_mode='Markdown', reply_markup=markup)