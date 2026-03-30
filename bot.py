import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============= جلب التوكن من متغيرات البيئة =============
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN في متغيرات البيئة")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# ============= زخارف الاسم =============

# زخارف عربية
arabic_styles = [
    {"func": lambda x: f"『{x}』", "emoji": "📦"},
    {"func": lambda x: f"「{x}」", "emoji": "🎋"},
    {"func": lambda x: f"【{x}】", "emoji": "🔲"},
    {"func": lambda x: f"★{x}★", "emoji": "⭐"},
    {"func": lambda x: f"☆{x}☆", "emoji": "✨"},
    {"func": lambda x: f"♡{x}♡", "emoji": "❤️"},
    {"func": lambda x: f"❥{x}", "emoji": "💕"},
    {"func": lambda x: f"✿{x}✿", "emoji": "🌸"},
    {"func": lambda x: f"༺{x}༻", "emoji": "👑"},
    {"func": lambda x: f"✧{x}✧", "emoji": "💎"},
    {"func": lambda x: f"☾{x}☽", "emoji": "🌙"},
    {"func": lambda x: f"⚡{x}⚡", "emoji": "⚡"},
    {"func": lambda x: f"🔥{x}🔥", "emoji": "🔥"},
    {"func": lambda x: f"꧁{x}꧂", "emoji": "🎨"},
    {"func": lambda x: f"⎯{x}⎯", "emoji": "📏"},
    {"func": lambda x: f"╰┈➤{x}", "emoji": "➡️"},
    {"func": lambda x: f"⛧{x}⛧", "emoji": "⛧"},
    {"func": lambda x: f"†{x}†", "emoji": "✝️"},
    {"func": lambda x: f"⚜️{x}⚜️", "emoji": "⚜️"},
    {"func": lambda x: f"𖤐{x}𖤐", "emoji": "🦋"},
    {"func": lambda x: f"『{x}』💫", "emoji": "💫"},
    {"func": lambda x: f"《{x}》", "emoji": "📖"},
    {"func": lambda x: f"〈{x}〉", "emoji": "🔹"},
    {"func": lambda x: f"「{x}」🔥", "emoji": "🔥"},
    {"func": lambda x: f"「{x}」✨", "emoji": "✨"},
    {"func": lambda x: f"『{x}』🌟", "emoji": "🌟"},
    {"func": lambda x: f"『{x}』💎", "emoji": "💎"},
]

# زخارف إنجليزية بخطوط مختلفة
def to_bold(text):
    bold_map = {'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
                'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
                'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
                'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙'}
    result = ""
    for char in text:
        if char.upper() in bold_map:
            result += bold_map[char.upper()] if char.isupper() else bold_map[char.upper()].lower()
        else:
            result += char
    return result

def to_script(text):
    script_map = {'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖',
                  'H': '𝓗', 'I': '𝓘', 'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝',
                  'O': '𝓞', 'P': '𝓟', 'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤',
                  'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩'}
    result = ""
    for char in text:
        if char.upper() in script_map:
            result += script_map[char.upper()] if char.isupper() else script_map[char.upper()].lower()
        else:
            result += char
    return result

def to_double(text):
    double_map = {'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽', 'G': '𝔾',
                  'H': 'ℍ', 'I': '𝕀', 'J': '𝕁', 'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ',
                  'O': '𝕆', 'P': 'ℙ', 'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋', 'U': '𝕌',
                  'V': '𝕍', 'W': '𝕎', 'X': '𝕏', 'Y': '𝕐', 'Z': 'ℤ'}
    result = ""
    for char in text:
        if char.upper() in double_map:
            result += double_map[char.upper()] if char.isupper() else double_map[char.upper()].lower()
        else:
            result += char
    return result

def to_fraktur(text):
    fraktur_map = {'A': '𝔄', 'B': '𝔅', 'C': 'ℭ', 'D': '𝔇', 'E': '𝔈', 'F': '𝔉', 'G': '𝔊',
                   'H': 'ℌ', 'I': 'ℑ', 'J': '𝔍', 'K': '𝔎', 'L': '𝔏', 'M': '𝔐', 'N': '𝔑',
                   'O': '𝔒', 'P': '𝔓', 'Q': '𝔔', 'R': 'ℜ', 'S': '𝔖', 'T': '𝔗', 'U': '𝔘',
                   'V': '𝔙', 'W': '𝔚', 'X': '𝔛', 'Y': '𝔜', 'Z': 'ℨ'}
    result = ""
    for char in text:
        if char.upper() in fraktur_map:
            result += fraktur_map[char.upper()] if char.isupper() else fraktur_map[char.upper()].lower()
        else:
            result += char
    return result

def to_mono(text):
    mono_map = {'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶',
                'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽',
                'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄',
                'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉'}
    result = ""
    for char in text:
        if char.upper() in mono_map:
            result += mono_map[char.upper()] if char.isupper() else mono_map[char.upper()].lower()
        else:
            result += char
    return result

def to_bubble(text):
    result = ""
    for char in text.upper():
        if 'A' <= char <= 'Z':
            result += chr(127280 + ord(char) - ord('A'))
        else:
            result += char
    return result

def to_square(text):
    result = ""
    for char in text.upper():
        if 'A' <= char <= 'Z':
            result += chr(127312 + ord(char) - ord('A'))
        else:
            result += char
    return result

english_styles = [
    {"func": lambda x: f"『{x}』", "emoji": "📦"},
    {"func": lambda x: f"「{x}」", "emoji": "🎋"},
    {"func": lambda x: f"★{x}★", "emoji": "⭐"},
    {"func": lambda x: f"♡{x}♡", "emoji": "❤️"},
    {"func": lambda x: f"✦{x}✦", "emoji": "✨"},
    {"func": to_bold, "emoji": "💪"},
    {"func": to_script, "emoji": "✍️"},
    {"func": to_double, "emoji": "2️⃣"},
    {"func": to_fraktur, "emoji": "🏰"},
    {"func": to_mono, "emoji": "⌨️"},
    {"func": to_bubble, "emoji": "💭"},
    {"func": to_square, "emoji": "🔲"},
    {"func": lambda x: f"༺{x}༻", "emoji": "👑"},
    {"func": lambda x: f"⚡{x}⚡", "emoji": "⚡"},
    {"func": lambda x: f"🔥{x}🔥", "emoji": "🔥"},
    {"func": lambda x: f"꧁{x}꧂", "emoji": "🎨"},
]

# ============= أزرار =============

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🇸🇦 زخرفة عربية", callback_data="arabic")
    btn2 = InlineKeyboardButton("🇬🇧 زخرفة إنجليزية", callback_data="english")
    markup.add(btn1, btn2)
    return markup

def get_more_button(name, lang):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("⏩ المزيد", callback_data=f"more_{lang}_{name}")
    btn2 = InlineKeyboardButton("🔁 اسم جديد", callback_data="new")
    markup.add(btn1, btn2)
    return markup

# ============= تخزين مؤقت للأسماء =============
user_names = {}

# ============= أوامر البوت =============

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "✨ **مرحباً بك في بوت الزخرفة المتقدم!** ✨\n\n"
        "📌 **أرسل اسمك أو أي نص تريد زخرفته**\n"
        "📌 **اختر نوع الزخرفة (عربي/إنجليزي)**\n"
        "📌 **اضغط على النص للنسخ المباشر**\n\n"
        "🎯 **أرسل النص الآن:**",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(message, save_name)

def save_name(message):
    """حفظ الاسم"""
    user_names[message.chat.id] = message.text
    bot.send_message(
        message.chat.id,
        f"✅ تم استلام: **{message.text}**\n\n"
        f"🎨 **اختر نوع الزخرفة:**",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    name = user_names.get(user_id, "")
    
    if not name:
        bot.edit_message_text(
            "⚠️ يرجى إرسال الاسم أولاً\nأرسل /start للبدء",
            call.message.chat.id,
            call.message.message_id
        )
        bot.answer_callback_query(call.id)
        return
    
    if call.data == "new":
        bot.edit_message_text(
            "📝 أرسل الاسم الجديد:",
            call.message.chat.id,
            call.message.message_id
        )
        bot.register_next_step_handler(call.message, save_name)
        bot.answer_callback_query(call.id)
        return
    
    if call.data == "arabic":
        styles = random.sample(arabic_styles, min(10, len(arabic_styles)))
        response = "🇸🇦 **زخارف عربية** 🇸🇦\n\n"
        for style in styles:
            response += f"{style['emoji']} {style['func'](name)}\n\n"
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_more_button(name, "arabic")
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == "english":
        styles = random.sample(english_styles, min(10, len(english_styles)))
        response = "🇬🇧 **زخارف إنجليزية** 🇬🇧\n\n"
        for style in styles:
            response += f"{style['emoji']} {style['func'](name)}\n\n"
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_more_button(name, "english")
        )
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith("more_"):
        parts = call.data.split("_", 2)
        lang = parts[1]
        name_text = parts[2]
        
        if lang == "arabic":
            styles = random.sample(arabic_styles, min(10, len(arabic_styles)))
            response = "🇸🇦 **المزيد من الزخارف العربية** 🇸🇦\n\n"
            for style in styles:
                response += f"{style['emoji']} {style['func'](name_text)}\n\n"
        else:
            styles = random.sample(english_styles, min(10, len(english_styles)))
            response = "🇬🇧 **المزيد من الزخارف الإنجليزية** 🇬🇧\n\n"
            for style in styles:
                response += f"{style['emoji']} {style['func'](name_text)}\n\n"
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=get_more_button(name_text, lang)
        )
        bot.answer_callback_query(call.id)

# ============= تشغيل البوت =============

if __name__ == "__main__":
    print("✅ بوت الزخرفة يعمل...")
    print(f"🤖 @{bot.get_me().username}")
    bot.infinity_polling()
