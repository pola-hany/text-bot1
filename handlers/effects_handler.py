from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db_manager import Database

db = Database()
user_texts = {}

def register_effects_handlers(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda call: call.data == "effects")
    def effects_callback(call):
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("📏 خط تحت", callback_data="effect_underline")
        btn2 = InlineKeyboardButton("✂️ خط وسط", callback_data="effect_strikethrough")
        btn3 = InlineKeyboardButton("🔄 نص مقلوب", callback_data="effect_reverse")
        btn4 = InlineKeyboardButton("␣ مسافات", callback_data="effect_spaces")
        btn5 = InlineKeyboardButton("📦 مربع", callback_data="effect_box")
        btn6 = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        
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
        effect = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"📝 أرسل النص لتطبيق التأثير")
        msg = bot.send_message(
            call.message.chat.id,
            f"🎨 **أرسل النص لتطبيق التأثير:**\n\n✨ التأثير المختار: **{get_effect_name(effect)}**",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, lambda m: apply_effect(bot, m, effect))
    
    def apply_effect(bot, message, effect):
        text = message.text
        result = get_effect_result(text, effect)
        
        msg_text = f"🎨 **نتيجة التأثير:**\n\n`{result}`"
        
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("🔄 تجربة مرة أخرى", callback_data="effects")
        btn2 = InlineKeyboardButton("🔙 القائمة", callback_data="back_to_menu")
        markup.add(btn1, btn2)
        
        bot.send_message(message.chat.id, msg_text, parse_mode='Markdown', reply_markup=markup)
        db.update_user_activity(message.from_user.id, "effects")

def get_effect_name(effect):
    names = {
        "underline": "خط تحت",
        "strikethrough": "خط وسط",
        "reverse": "نص مقلوب",
        "spaces": "مسافات بين الحروف",
        "box": "مربع"
    }
    return names.get(effect, effect)

def get_effect_result(text, effect):
    if effect == "underline":
        return f"<u>{text}</u>"
    elif effect == "strikethrough":
        return f"<s>{text}</s>"
    elif effect == "reverse":
        return text[::-1]
    elif effect == "spaces":
        return " ".join(text)
    elif effect == "box":
        return f"┌───┐\n│{text}│\n└───┘"
    return text