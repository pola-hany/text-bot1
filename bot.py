import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random
import string
import re

# ضع التوكن الخاص بك هنا
TOKEN = "8633043777:AAHPtW9zkm_vfiCuN917UzcBNt7tFdJoWo8"
bot = telebot.TeleBot(TOKEN)

# ==================== قواميس الزخرفة ====================

# زخارف عربية
arabic_decorations = [
    lambda x: f"『 {x} 』", lambda x: f"「 {x} 」", lambda x: f"【 {x} 】",
    lambda x: f"★ {x} ★", lambda x: f"✨{x}✨", lambda x: f"♡ {x} ♡",
    lambda x: f"❥ {x}", lambda x: f"༺ {x} ༻", lambda x: f"✧ {x} ✧",
    lambda x: f"☾ {x} ☽", lambda x: f"『{x}』💫", lambda x: f"《 {x} 》",
    lambda x: f"〈 {x} 〉", lambda x: f"⎯ {x} ⎯", lambda x: f"╰┈➤ {x}",
    lambda x: f"⛧ {x} ⛧", lambda x: f"† {x} †", lambda x: f"⚜️ {x} ⚜️",
    lambda x: f"「{x}」🔥", lambda x: f"✿ {x} ✿"
]

# زخارف إنجليزية
english_decorations = [
    lambda x: f"『 {x} 』", lambda x: f"「 {x} 」", lambda x: f"【 {x} 】",
    lambda x: f"★ {x} ★", lambda x: f"✨{x}✨", lambda x: f"♡ {x} ♡",
    lambda x: f"❥ {x}", lambda x: f"༺ {x} ༻", lambda x: f"✧ {x} ✧",
    lambda x: f"☾ {x} ☽", lambda x: f"𝕋𝕙𝕖 {x}", lambda x: f"🅃🄷🄴 {x.upper()}",
    lambda x: f"𝓣𝓱𝓮 {x}", lambda x: f"𝕿𝖍𝖊 {x}", lambda x: f"ᵗʰᵉ {x}",
    lambda x: f"🇹 🇭 🇪  {x}", lambda x: f"Ⓣⓗⓔ {x}", lambda x: f"🅣🅗🅔 {x}"
]

# تأثيرات إضافية
def add_underline(text): return f"<u>{text}</u>"
def add_overline(text): return f"<u>{text}</u>"  # Telegram doesn't support overline directly
def add_strikethrough(text): return f"<s>{text}</s>"
def reverse_text(text): return text[::-1]
def add_spaces(text): return " ".join(text)
def add_box(text): return f"┌───┐\n│{text}│\n└───┘"

# ==================== بايوهات جاهزة ====================

whatsapp_bios = [
    "✨ الحياة بسيطة، لا تعقدها ✨",
    "💫 توكل على الله وتحرك 💫",
    "❤️ عيش حياتك بلا أسف ❤️",
    "🌙 لست متاحًا للجميع 🌙",
    "🔥 لا تقارنني بأحد 🔥",
    "🎯 راضي بقسمتي 🎯",
    "🕊️ سلام داخلي 🕊️",
    "⭐ تحت الإشراف الإلهي ⭐"
]

instagram_bios = [
    "📸 | Just vibes ✨",
    "💫 | Living my best life",
    "❤️ | Love & Peace",
    "🎯 | Dream chaser",
    "🌙 | Night owl",
    "🔥 | Hustle mode",
    "🕊️ | Free soul",
    "⭐ | Star stuff"
]

messenger_bios = [
    "💬 | متاح للكلام أحيانًا",
    "🎮 | Gaming mode on",
    "📱 | Offline life online",
    "💭 | أفكار عشوائية",
    "🎧 | Music is life",
    "📚 | قراءة وكتابة",
    "🌍 | عابر سبيل",
    "⚡ | سريع الاستجابة"
]

# ==================== دوال مساعدة ====================

def get_random_decorations(text, lang, count=10):
    decorations = arabic_decorations if lang == 'arabic' else english_decorations
    selected = random.sample(decorations, min(count, len(decorations)))
    results = []
    emojis = ['✨', '🌟', '💫', '⭐', '🔥', '❤️', '💙', '💜', '🖤', '💛']
    for i, dec in enumerate(selected):
        results.append(f"{emojis[i % len(emojis)]} {dec(text)}")
    return results

def get_translations(name):
    # محاكاة للترجمة (لأغراض العرض)
    korean_map = {
        'ا': '아', 'ب': '바', 'ت': '타', 'ث': '사', 'ج': '자', 'ح': '하',
        'خ': '카', 'د': '다', 'ذ': '자', 'ر': '라', 'ز': '자', 'س': '사',
        'ش': '샤', 'ص': '사', 'ض': '다', 'ط': '타', 'ظ': '자', 'ع': '아',
        'غ': '가', 'ف': '파', 'ق': '카', 'ك': '카', 'ل': '라', 'م': '마',
        'ن': '나', 'ه': '하', 'و': '와', 'ي': '야'
    }
    
    chinese_map = {
        'ا': '阿', 'ب': '巴', 'ت': '塔', 'ث': '萨', 'ج': '贾', 'ح': '哈',
        'خ': '哈', 'د': '达', 'ذ': '扎', 'ر': '拉', 'ز': '扎', 'س': '萨',
        'ش': '沙', 'ص': '萨', 'ض': '达', 'ط': '塔', 'ظ': '扎', 'ع': '阿',
        'غ': '加', 'ف': '法', 'ق': '卡', 'ك': '卡', 'ل': '拉', 'م': '马',
        'ن': '纳', 'ه': '哈', 'و': '瓦', 'ي': '亚'
    }
    
    korean_name = ''.join([korean_map.get(ch, ch) for ch in name])
    chinese_name = ''.join([chinese_map.get(ch, ch) for ch in name])
    
    return korean_name, chinese_name

# ==================== أزرار ====================

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("✨ زخرفة النصوص", callback_data="decorate")
    btn2 = InlineKeyboardButton("🌍 تحويل الاسم", callback_data="translate")
    btn3 = InlineKeyboardButton("📝 بايوهات جاهزة", callback_data="bios")
    btn4 = InlineKeyboardButton("🎨 تأثيرات إضافية", callback_data="effects")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def lang_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🇸🇦 عربي", callback_data="lang_arabic")
    btn2 = InlineKeyboardButton("🇬🇧 إنجليزي", callback_data="lang_english")
    markup.add(btn1, btn2)
    return markup

def bio_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("💚 واتساب", callback_data="bio_whatsapp")
    btn2 = InlineKeyboardButton("📸 إنستجرام", callback_data="bio_instagram")
    btn3 = InlineKeyboardButton("💬 ماسنجر", callback_data="bio_messenger")
    btn4 = InlineKeyboardButton("🔙 رجوع", callback_data="back")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def effect_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("📏 خط تحت", callback_data="effect_underline")
    btn2 = InlineKeyboardButton("✂️ خط وسط", callback_data="effect_strike")
    btn3 = InlineKeyboardButton("🔄 نص مقلوب", callback_data="effect_reverse")
    btn4 = InlineKeyboardButton("␣ مسافات", callback_data="effect_spaces")
    btn5 = InlineKeyboardButton("📦 مربع", callback_data="effect_box")
    btn6 = InlineKeyboardButton("🔙 رجوع", callback_data="back")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# ==================== أوامر البوت ====================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """
🌟 **مرحبًا بك في بوت الزخرفة المتقدم!** 🌟

📌 **أرسل أي نص وسأقوم بزخرفته لك**
📌 **اختر من القائمة ما يناسبك**

✅ **جميع النصوص قابلة للنسخ بالضغط عليها مباشرة**
"""
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "decorate":
        bot.answer_callback_query(call.id, "📝 أرسل النص الآن")
        msg = bot.send_message(call.message.chat.id, "📝 **أرسل النص الذي تريد زخرفته:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, ask_lang)
    
    elif call.data == "translate":
        bot.answer_callback_query(call.id, "🌍 أرسل الاسم الآن")
        msg = bot.send_message(call.message.chat.id, "🌍 **أرسل الاسم (عربي أو إنجليزي) لتحويله:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, show_translations)
    
    elif call.data == "bios":
        bot.edit_message_text("📝 **اختر نوع البايو:**", call.message.chat.id, call.message.message_id, reply_markup=bio_menu())
    
    elif call.data == "effects":
        bot.edit_message_text("🎨 **اختر التأثير المطلوب:**\n\n📌 أرسل النص أولاً ثم اختر التأثير", 
                              call.message.chat.id, call.message.message_id, reply_markup=effect_menu())
    
    elif call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        user_text = get_user_text(call.message.chat.id)
        if user_text:
            show_decorations(call.message.chat.id, user_text, lang, call.message.message_id)
        else:
            bot.send_message(call.message.chat.id, "⚠️ يرجى إرسال النص أولاً")
    
    elif call.data.startswith("bio_"):
        bio_type = call.data.split("_")[1]
        show_bios(call.message.chat.id, bio_type, call.message.message_id)
    
    elif call.data.startswith("effect_"):
        effect = call.data.split("_")[1]
        bot.answer_callback_query(call.id, "📝 أرسل النص الآن")
        msg = bot.send_message(call.message.chat.id, f"🎨 **أرسل النص لتطبيق التأثير:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, lambda m: apply_effect(m, effect))
    
    elif call.data == "back":
        bot.edit_message_text("🌟 **القائمة الرئيسية:**", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    
    elif call.data.startswith("more_"):
        _, text, lang, offset = call.data.split("|")
        show_more_decorations(call.message.chat.id, text, lang, int(offset), call.message.message_id)
    
    elif call.data.startswith("refresh_"):
        _, bio_type = call.data.split("|")
        show_bios(call.message.chat.id, bio_type, call.message.message_id)

# ==================== دوال رئيسية ====================

user_texts = {}

def get_user_text(chat_id):
    return user_texts.get(chat_id, None)

def ask_lang(message):
    user_texts[message.chat.id] = message.text
    bot.send_message(message.chat.id, "🗣️ **اختر لغة الزخرفة:**", parse_mode='Markdown', reply_markup=lang_menu())

def show_decorations(chat_id, text, lang, msg_id=None):
    decorations = get_random_decorations(text, lang, 10)
    response = "✨ **زخارفك:** ✨\n\n" + "\n\n".join(decorations)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⏩ المزيد", callback_data=f"more_{text}|{lang}|10"))
    markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    
    if msg_id:
        bot.edit_message_text(response, chat_id, msg_id, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=markup)

def show_more_decorations(chat_id, text, lang, offset, msg_id):
    new_decorations = get_random_decorations(text, lang, 10)
    response = "✨ **زخارف إضافية:** ✨\n\n" + "\n\n".join(new_decorations)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⏩ المزيد", callback_data=f"more_{text}|{lang}|{offset+10}"))
    markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    bot.edit_message_text(response, chat_id, msg_id, parse_mode='Markdown', reply_markup=markup)

def show_translations(message):
    name = message.text
    korean, chinese = get_translations(name)
    
    response = f"🌍 **تحويل الاسم:** 🌍\n\n"
    response += f"🇰🇷 **كوري:**\n`{korean}`\n\n"
    response += f"🇨🇳 **صيني:**\n`{chinese}`"
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

def show_bios(chat_id, bio_type, msg_id=None):
    if bio_type == "whatsapp":
        bios = random.sample(whatsapp_bios, min(5, len(whatsapp_bios)))
        title = "💚 **بايوهات واتساب:** 💚"
    elif bio_type == "instagram":
        bios = random.sample(instagram_bios, min(5, len(instagram_bios)))
        title = "📸 **بايوهات إنستجرام:** 📸"
    else:
        bios = random.sample(messenger_bios, min(5, len(messenger_bios)))
        title = "💬 **بايوهات ماسنجر:** 💬"
    
    response = title + "\n\n" + "\n\n".join(bios)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 تغيير", callback_data=f"refresh_{bio_type}"))
    markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="bios"))
    
    if msg_id:
        bot.edit_message_text(response, chat_id, msg_id, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=markup)

def apply_effect(message, effect):
    text = message.text
    result = ""
    
    if effect == "underline":
        result = f"<u>{text}</u>"
    elif effect == "strike":
        result = f"<s>{text}</s>"
    elif effect == "reverse":
        result = text[::-1]
    elif effect == "spaces":
        result = " ".join(text)
    elif effect == "box":
        result = f"┌───┐\n│{text}│\n└───┘"
    
    bot.send_message(message.chat.id, f"🎨 **النتيجة:**\n\n`{result}`", parse_mode='Markdown')

# ==================== تشغيل البوت ====================

if __name__ == "__main__":
    print("✅ البوت يعمل الآن...")
    bot.infinity_polling()
