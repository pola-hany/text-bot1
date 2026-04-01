import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from fonts.korean_fonts import KOREAN_STYLES
from fonts.chinese_fonts import CHINESE_STYLES
from fonts.egyptian_fonts import EGYPTIAN_STYLES

# تخزين أسماء المستخدمين للترجمة
user_texts = {}

def register_translation_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "translate")
    def translate_callback(call):
        """طلب الترجمة"""
        bot.answer_callback_query(call.id, "🌍 أرسل النص للترجمة")
        msg = bot.send_message(
            call.message.chat.id,
            "🌍 **أرسل الاسم أو النص للترجمة:**\n\n"
            "📌 يمكنك إرسال:\n"
            "• اسم بالعربية\n"
            "• اسم بالإنجليزية\n\n"
            "✅ سيتم عرض الترجمات بعد إرسال النص",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, ask_translation_lang)
    
    def ask_translation_lang(message):
        """سؤال المستخدم عن لغة الترجمة"""
        user_texts[message.chat.id] = message.text
        
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("🇰🇷 كوري", callback_data=f"trans_korean_{message.chat.id}")
        btn2 = InlineKeyboardButton("🇨🇳 صيني", callback_data=f"trans_chinese_{message.chat.id}")
        btn3 = InlineKeyboardButton("𓂀 فرعوني", callback_data=f"trans_egyptian_{message.chat.id}")
        markup.add(btn1, btn2, btn3)
        
        bot.send_message(
            message.chat.id,
            f"✅ تم استلام: **{message.text}**\n\n"
            f"🌍 **اختر لغة الترجمة:**",
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("trans_"))
    def handle_translation(call):
        """معالج اختيار لغة الترجمة"""
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
        
        bot.answer_callback_query(call.id, f"✨ جاري الترجمة...")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("more_trans_"))
    def handle_more_translations(call):
        """المزيد من الترجمات"""
        parts = call.data.split("_")
        lang = parts[2]
        user_id = int(parts[3])
        text = user_texts.get(user_id, "")
        
        if not text:
            bot.answer_callback_query(call.id, "⚠️ يرجى إعادة إرسال النص", show_alert=True)
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        if lang == "korean":
            send_korean_translations(bot, call.message.chat.id, text)
        elif lang == "chinese":
            send_chinese_translations(bot, call.message.chat.id, text)
        else:
            send_egyptian_translations(bot, call.message.chat.id, text)
        
        bot.answer_callback_query(call.id, "✨ جاري توليد المزيد...")

def send_korean_translations(bot, chat_id, text):
    """إرسال الترجمات الكورية"""
    selected = random.sample(KOREAN_STYLES, min(8, len(KOREAN_STYLES)))
    
    for style in selected:
        try:
            translated = style["func"](text)
            msg_text = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg_text, parse_mode='Markdown')
        except Exception as e:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_trans_korean_{chat_id}")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="translate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        chat_id,
        "🇰🇷 **للحصول على المزيد من الترجمات الكورية:**",
        parse_mode='Markdown',
        reply_markup=markup
    )

def send_chinese_translations(bot, chat_id, text):
    """إرسال الترجمات الصينية"""
    selected = random.sample(CHINESE_STYLES, min(8, len(CHINESE_STYLES)))
    
    for style in selected:
        try:
            translated = style["func"](text)
            msg_text = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg_text, parse_mode='Markdown')
        except Exception as e:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_trans_chinese_{chat_id}")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="translate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        chat_id,
        "🇨🇳 **للحصول على المزيد من الترجمات الصينية:**",
        parse_mode='Markdown',
        reply_markup=markup
    )

def send_egyptian_translations(bot, chat_id, text):
    """إرسال الترجمات الفرعونية"""
    selected = random.sample(EGYPTIAN_STYLES, min(8, len(EGYPTIAN_STYLES)))
    
    for style in selected:
        try:
            translated = style["func"](text)
            msg_text = f"{style['emoji']} **{style['name']}**\n`{translated}`\n_{style['desc']}_"
            bot.send_message(chat_id, msg_text, parse_mode='Markdown')
        except Exception as e:
            continue
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_trans_egyptian_{chat_id}")
    btn2 = InlineKeyboardButton("🔄 نص جديد", callback_data="translate")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        chat_id,
        "𓂀 **للحصول على المزيد من الترجمات الفرعونية:**",
        parse_mode='Markdown',
        reply_markup=markup
    )