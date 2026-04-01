from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# تخزين النصوص للتأثيرات
user_texts = {}

def register_effects_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "effects")
    def effects_callback(call):
        """عرض قائمة التأثيرات"""
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("📏 خط تحت", callback_data="effect_underline")
        btn2 = InlineKeyboardButton("✂️ خط وسط", callback_data="effect_strikethrough")
        btn3 = InlineKeyboardButton("🔄 نص مقلوب", callback_data="effect_reverse")
        btn4 = InlineKeyboardButton("␣ مسافات", callback_data="effect_spaces")
        btn5 = InlineKeyboardButton("📦 مربع", callback_data="effect_box")
        btn6 = InlineKeyboardButton("✨ خط علوي", callback_data="effect_overline")
        btn7 = InlineKeyboardButton("🔙 رجوع", callback_data="menu")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        markup.add(btn7)
        
        bot.edit_message_text(
            "🎨 **اختر التأثير المطلوب:**",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("effect_"))
    def apply_effect_callback(call):
        """طلب إدخال النص للتأثير"""
        effect = call.data.split("_")[1]
        
        bot.answer_callback_query(call.id, f"📝 أرسل النص لتطبيق التأثير")
        msg = bot.send_message(
            call.message.chat.id,
            f"🎨 **أرسل النص لتطبيق التأثير:**\n\n"
            f"✨ التأثير المختار: **{get_effect_name(effect)}**\n\n"
            f"📌 سيتم عرض النص بعد التأثير مباشرة",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, lambda m: apply_effect(bot, m, effect))
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("more_effect_"))
    def more_effect(call):
        """تطبيق نفس التأثير على نص جديد"""
        effect = call.data.split("_")[2]
        user_id = call.message.chat.id
        text = user_texts.get(user_id, "")
        
        if not text:
            bot.answer_callback_query(call.id, "⚠️ يرجى إرسال النص أولاً", show_alert=True)
            return
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_effect_result(bot, call.message.chat.id, text, effect)

def get_effect_name(effect):
    """الحصول على اسم التأثير بالعربي"""
    names = {
        "underline": "خط تحت",
        "strikethrough": "خط وسط",
        "reverse": "نص مقلوب",
        "spaces": "مسافات بين الحروف",
        "box": "مربع",
        "overline": "خط علوي"
    }
    return names.get(effect, effect)

def apply_effect(bot, message, effect):
    """تطبيق التأثير على النص"""
    text = message.text
    user_texts[message.chat.id] = text
    show_effect_result(bot, message.chat.id, text, effect)

def show_effect_result(bot, chat_id, text, effect):
    """عرض نتيجة التأثير"""
    result = ""
    emoji = ""
    
    if effect == "underline":
        result = f"<u>{text}</u>"
        emoji = "📏"
    elif effect == "strikethrough":
        result = f"<s>{text}</s>"
        emoji = "✂️"
    elif effect == "reverse":
        result = text[::-1]
        emoji = "🔄"
    elif effect == "spaces":
        result = " ".join(text)
        emoji = "␣"
    elif effect == "box":
        result = f"┌───┐\n│{text}│\n└───┘"
        emoji = "📦"
    elif effect == "overline":
        result = f"‾‾‾‾‾\n{text}\n_____"
        emoji = "✨"
    
    msg_text = f"{emoji} **نتيجة التأثير:**\n\n`{result}`"
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🔄 تجربة مرة أخرى", callback_data=f"more_effect_{effect}")
    btn2 = InlineKeyboardButton("🎨 تأثير آخر", callback_data="effects")
    btn3 = InlineKeyboardButton("🔙 القائمة", callback_data="menu")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        chat_id,
        msg_text,
        parse_mode='HTML',
        reply_markup=markup
    )